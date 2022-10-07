import argparse
import csv
import gzip
import numpy as np
import os
import sys
import time

from bloc.generator import add_bloc_sequences
from bloc.util import dumpJsonToFile
from bloc.util import getDictFromJson

from itertools import combinations
from random import shuffle

from sklearn.model_selection import StratifiedKFold
from statistics import mean, median

from util import get_social_fingerprint_frm_bloc
from util import get_social_fingerprint_influenced

from TwitterDNA.tdna import train_test_twitter_dna_model
from TwitterDNA.tdna_influenced import partition_lst
from TwitterDNA.tdna_influenced import train_test_twitter_dna_influenced_model

def get_generic_args():

    parser = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=30), description='Evaluate Twitter DNA and DNA-influenced methods')
    parser.add_argument('tweets_files', nargs='+', help='Filename/Path containing tweets to process. If filename (see --tweets-path)')

    parser.add_argument('-e', '--evaluate-models', nargs='+', default=['bloc', 'sf', 'sf-influenced', 'botometer-lite'], choices=['sf', 'sf-influenced'], help='Models to evaluate')
    parser.add_argument('--add-pauses', action='store_true', help='BLOC generator (for words not bigram) use pause as separate words in vocabulary True/False. False is default')
    parser.add_argument('--bloc-model', default='word', choices=['bigram', 'word'], help='BLOC tokenization method.')

    parser.add_argument('--no-merge', action='store_true', help='Do not merge dataset variants (e.g., "bot-A" and "bot-B") of sources into single class (e.g, "bot").')
    parser.add_argument('-o', '--outpath', default=os.getcwd() + '/Output/', help='Output path')
    parser.add_argument('-t', '--task', default='pca_general', choices=['evaluate'], help='Task to run')
    parser.add_argument('--tweets-path', default='/scratch/anwala/IU/BLOC/botometer_retraining_data', help='The path to extract tweets for --tweets-files.')
    
    #max parameters
    parser.add_argument('-m', '--max-tweets', type=int, default=100, help='Maximum number of tweets per user to consider')
    parser.add_argument('-n', '--min-tweets', type=int, default=20, help='Mininum number of tweets per user to consider')
    parser.add_argument('-u', '--max-users', type=int, default=300, help='Maximum number of users per class to process')
    
    #BLOC parameters
    parser.add_argument('--bc-bloc-alphabets', nargs='+', default=['action', 'content_syntactic'], choices=['action', 'content_syntactic', 'content_syntactic_with_pauses', 'change', 'action_content_syntactic'], help='add_bloc_sequences()\'s BLOC alphabets to extract')

    return parser

def get_eval_metric_frm_conf_mat(conf_mat):

    if( conf_mat.shape != (2, 2) ):
        return {}

    TP = conf_mat[0][0]
    TN = conf_mat[1][1]
    FP = conf_mat[0][1]
    FN = conf_mat[1][0]
    
    precision = TP/(TP+FP) if TP + FP != 0 else 0
    recall = TP/(TP+FN) if TP + FN != 0 else 0
    f1 = 2*((precision * recall)/(precision + recall)) if precision + recall != 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1-score': f1,
        'support': TP + TN + FP + FN
    }

def get_bloc_for_tweets(tweets_files, tweets_path, gen_bloc_params, **kwargs):

    print('\nget_bloc_for_tweets():')
    max_users = kwargs.get('max_users', 300)
    max_tweets = kwargs.get('max_tweets', 100)
    min_tweets = kwargs.get('min_tweets', 20)

    def get_user_id_class_map(f):

        user_id_class_map = {}
        all_classes = set()

        try:
            with open(cf) as fd:
                
                rd = csv.reader(fd, delimiter='\t')
                for user_id, user_class in rd:
                    user_id_class_map[user_id] = user_class
                    all_classes.add(user_class)
        except:
            genericErrorInfo()

        return user_id_class_map, all_classes

    def is_all_class_full(all_users, max_users):

        for c in all_users:
            if( len(all_users[c]) != max_users ):
                return False

        return True


    payload = {}
    for f in tweets_files:

        f = tweets_path + f + '/tweets.jsons.gz' if f.find('tweets') == -1 else f
        cf = '/'.join( f.split('/')[:-1] ) + '/userIds.txt'
        src = f.split('/')[-2]
        
        print('tweets file:', f)
        print('src:', src)
        
        if( os.path.exists(f) is False ):
            print('\ttweets file doesn\'t exist, returning')
            continue

        user_id_class_map, all_classes = get_user_id_class_map( cf )
        print('all_classes:', all_classes)
        if( len(user_id_class_map) == 0 ):
            print('\tuser_id_class_map is empty, returning')
            continue
        
        users_tweets = {}
        for c in all_classes:
            users_tweets[c] = []

        encoding = None
        if( src.find('stock') != -1 ):
            encoding = 'windows-1252'

        with gzip.open(f, 'rt', encoding=encoding) as infile:
            for line in infile:
                try:

                    line = line.split('\t')
                    '''
                        line[0]: user_id
                        line[1]: tweets
                    '''
                    if( len(line) != 2 ):
                        continue

                    user_class = user_id_class_map.get(line[0], '')
                    if( user_class == '' ):
                        continue
                    
                    tweets = getDictFromJson( line[1] )
                    if( len(tweets) < min_tweets ):
                        continue
                    
                    if( is_all_class_full(users_tweets, max_users) ):
                        break

                    count = len( users_tweets[user_class] )
                    if( count == max_users ):
                        continue

                    tweets = tweets if max_tweets == -1 else tweets[:max_tweets]
                    screen_name = tweets[0]['user']['screen_name']
                    user_id = tweets[0]['user']['id']

                    bloc_payload = add_bloc_sequences(tweets, **gen_bloc_params)
                    bloc_payload['single_tweet'] = tweets[0]

                    
                    if( count % 100 == 0 ):
                        print( f'\t{count} of {max_users} {user_class} users' )

                    users_tweets[user_class].append( bloc_payload )
                except:
                    genericErrorInfo()


        payload[src] = users_tweets

    return payload

def get_train_test_strat_kfold_splits(doc_lst, k_folds=10):

    train_test_split_indices = []
    
    if( len(doc_lst) > k_folds ):

        class_labels = [ u['class'] for u in doc_lst ]
        skf = StratifiedKFold( n_splits=k_folds, shuffle=True )
        
        for train_index, test_index in skf.split(doc_lst, class_labels):
            train_test_split_indices.append( (train_index, test_index) )
    else:
        print('\tCannot have number of splits k_folds={} greater than the number of samples: n_samples={}.'.format(k_folds, len(doc_lst)) )
        return []

    return train_test_split_indices

def get_doc_lst_model(doc_lst, model, model_dims):
        
    mod_doc_lst = []
    
    for d in doc_lst:
        

        doc = [ d[model][dim] for dim in model_dims if dim in d[model] ]
        if( len(doc) == 0 ):
            continue

        doc = ' * '.join(doc)
        doc = doc.strip()
    
        if( doc == '' ):
            continue

        mod_doc_lst.append({
            'text': doc,
            'screen_name': d['screen_name'],
            'single_tweet': d['single_tweet'],
            'user_id': d['user_id'],
            'class': d['class'],
            'src': d['src']
        })

    return mod_doc_lst

def run_single_tdna_expr(sf_alphabet, model_variant, doc_lst, k_folds, all_conf_mat, start_offset=250):

    train_test_split_indices = get_train_test_strat_kfold_splits(doc_lst, k_folds=k_folds)
    if( len(train_test_split_indices) == 0 ):
        return all_conf_mat

    pos_neg_class = {'non_bot_class': 'human', 'bot_class': 'bot'}

    for train_index, test_index in train_test_split_indices:
    
        ori_train = [ doc_lst[indx] for indx in train_index ]
        ori_test = [ doc_lst[indx] for indx in test_index ]
        
        #sf_alphabet: b3_type, b3_content, b6_content
        sf_training_set = get_doc_lst_model( ori_train, model_variant, [sf_alphabet] )
        sf_test_set = get_doc_lst_model( ori_test, model_variant, [sf_alphabet] )

        if( model_variant == 'sf' ):
            tdna_class_rep = train_test_twitter_dna_model( pos_neg_class, sf_training_set, sf_test_set, start_offset )
        else:
            tdna_class_rep = train_test_twitter_dna_influenced_model( pos_neg_class, sf_training_set, sf_test_set )

        if( 'confusion_matrix' in tdna_class_rep ):
            all_conf_mat += tdna_class_rep['confusion_matrix']

    return all_conf_mat


def task_evaluate_models(all_eval_doc_lst, bloc_model, evaluate_models, args):

    print('\ntask_evaluate_models():')
    print('\tevaluate_models:', evaluate_models)
    print('\tadd_pauses:', args.add_pauses)

    expr_models = [
        {'model_name': 'b3_type', 'model': 'dna', 'alphabet': 'b3_type', 'model_variant': 'sf'},
        {'model_name': 'b3_content', 'model': 'dna', 'alphabet': 'b3_content', 'model_variant': 'sf'},
        {'model_name': 'b6_content', 'model': 'dna', 'alphabet': 'b6_content', 'model_variant': 'sf'},
        {'model_name': 'sf_influenced', 'model': 'dna_influenced', 'alphabet': 'sf_influenced', 'model_variant': 'sf_influenced'}
    ]

    k_folds = 5
    start_offset = 1
    
    for i in range( len(expr_models) ):
        
        model = expr_models[i]['model']
        all_conf_mat = np.zeros( (2, 2) )
        
        all_conf_mat = run_single_tdna_expr(expr_models[i]['alphabet'], expr_models[i]['model_variant'], all_eval_doc_lst, k_folds, all_conf_mat, start_offset=start_offset)
        expr_models[i]['eval_report'] = get_eval_metric_frm_conf_mat(all_conf_mat)

        print('model:', model)
        print(all_conf_mat)
        print(expr_models[i]['eval_report'])
        print()
        print()

    dumpJsonToFile('bot_detection_results.json', expr_models)
    print('\nWrote: bot_detection_results.json')

def run_tasks(dataset, args):

    parenth_flag = '' if ('action_content_syntactic' in args.bc_bloc_alphabets or 'content_syntactic_with_pauses' in args.bc_bloc_alphabets) else '()'
    pause_flag = '|[□⚀⚁⚂⚃⚄⚅]' if args.add_pauses is True else ''
    word_token_pattern = f'[^□⚀⚁⚂⚃⚄⚅ |*{parenth_flag}]+{pause_flag}'
    
    print(f'\nrun_task: {args.task}')
    print(f'\tbloc alphabets: {args.bc_bloc_alphabets}')
    print(f'\tword_token_pattern:', word_token_pattern)


    bloc_models = {
        'bigram': {
            'name': 'bigram',
            'ngram': 2,
            'token_pattern': '[^ |()*]',
            'bloc_variant': None,
            'dimensions': args.bc_bloc_alphabets
        },
        'word': {
            'name': 'word',
            'ngram': 1,
            'token_pattern': word_token_pattern,
            'bloc_variant': {'type': 'folded_words', 'fold_start_count': 4, 'count_applies_to_all_char': False},
            'dimensions': args.bc_bloc_alphabets
        }
    }
    
    if( args.task == 'pca_pairs' ):
        task_pca_pairs(dataset, bloc_models[args.bloc_model])
    elif( args.task == 'pca_general' ):
        task_pca_general(dataset, bloc_models[args.bloc_model])
    elif( args.task == 'top_k_words' ):
        task_top_k_words(dataset, bloc_models[args.bloc_model], args.outpath)
    elif( args.task == 'evaluate' ):
        task_evaluate_models(dataset, bloc_models[args.bloc_model], args.evaluate_models, args)

def rename_cols(all_datasets, src_map):

    print('\trename_cols():')

    for old_src, new_src in src_map:
        
        if( old_src not in all_datasets ):
            continue

        print(f'\trenaming {old_src} with {new_src}')
        all_datasets[new_src] = all_datasets.pop(old_src)

def merge_srcs(all_datasets, merge_lst, max_users):
    
    if( len(merge_lst) == 0 ):
        return
    
    print('\nmerge_srcs():')
    for i in range( len(merge_lst) ):
        
        src = merge_lst[i]['src']
        new_class = merge_lst[i]['new_class']

        if( src not in all_datasets ):
            continue

        print( '\tsrc:', src )
        print( '\tmerging all {} to {}'.format(merge_lst[i]['old_classes'], new_class) )
        print()

        new_cols = []
        new_size = max_users//len(merge_lst[i]['old_classes'])
        for c in merge_lst[i]['old_classes']:

            if( c not in all_datasets[src] ):
                continue

            new_cols += all_datasets[src][c][:new_size]
            del all_datasets[src][c]
        
        all_datasets[src][new_class] = new_cols

def add_more_details(all_datasets, add_dna_influenced=False):

    def add_sf(user):

        sf_docs = {}
        for dim in ['content_syntactic', 'action']:
            
            if( dim not in user['bloc'] ):
                continue

            sf_payload = get_social_fingerprint_frm_bloc( user['bloc'][dim], dimension=dim )
            for sf_type in sf_payload:
                sf_docs[ sf_type.pop('type') ] = sf_type.pop('text')

        user['sf'] = sf_docs

    for src, payload in all_datasets.items():
        for classs, users in payload.items():
            for i in range( len(users) ):

                users[i]['src'] = src
                users[i]['class'] = classs

                if( 'action_post_ref_time' in users[i]['bloc'] ):
                    del users[i]['bloc']['action_post_ref_time']
                
                if( add_dna_influenced and 'action_content_syntactic' in users[i]['bloc'] ):
                    
                    sfi_payload = get_social_fingerprint_influenced( users[i]['bloc']['action_content_syntactic'], dimension='action_content_syntactic' )
                    users[i]['sf_influenced'] = {}
                    for sfi_type in sfi_payload:
                        users[i]['sf_influenced'][ sfi_type.pop('type') ] = sfi_type.pop('text')

                    print('\nDNA Influenced is on, added sf_influenced to user, now deleting action_content_syntactic')
                    del users[i]['bloc']['action_content_syntactic']

                add_sf( users[i] )

def flatten_dataset_shuffle(all_datasets):

    print('\nflatten_dataset_shuffle()')
    print('pre flatten report')

    min_class_count = {}
    users_per_class = {}
    for src, payload in all_datasets.items():
        print(f'\tsrc: {src}')
        for classs, users in payload.items():
            print(f'\t\tclass: {classs}', len(users), 'users')
            
            users_per_class[classs] = []
            min_class_count.setdefault(classs, 0)
            min_class_count[classs] += len(users)
    

    for src, payload in all_datasets.items():
        for classs, users in payload.items():
            users_per_class[classs] += users

    min_class_count = sorted( min_class_count.items(), key=lambda item: item[1] )[0][1]
    print('class counts:')
    print('min_class_count:', min_class_count)
    flat_ds = []
    for c in users_per_class:
        print('\t', c, len(users_per_class[c]), 'users')
        shuffle(users_per_class[c])
        flat_ds += users_per_class[c][:min_class_count]
        users_per_class[c] = 0

    
    print()
    print('final dist:')
    src_dist = {}
    for u in flat_ds:
        users_per_class[ u['class'] ] += 1
        src_dist.setdefault(u['src'], 0)
        src_dist[ u['src'] ] += 1
    
    print('users_per_class:', users_per_class)
    print('src_dist:')
    for src, cnt in src_dist.items():
        print('\tsrc:', src, cnt)

    return flat_ds

def main():
    
    parser = get_generic_args()
    args = parser.parse_args()

    if( 'action_content_syntactic' in args.bc_bloc_alphabets and args.task in ['pca_pairs', 'pca_general', 'top_k_words'] ):
        #avoid mixing action_content_syntactic with other alphabets
        args.bc_bloc_alphabets = ['action_content_syntactic']

    if( 'sf-influenced' in args.evaluate_models ):
        print('\nDNA Influenced is on, adding action_content_syntactic to args.bc_bloc_alphabets')
        args.bc_bloc_alphabets += ['action_content_syntactic']
        args.bc_bloc_alphabets = list(set(args.bc_bloc_alphabets))
    

    args.tweets_path = args.tweets_path.strip() if args.tweets_path.strip().endswith('/') else args.tweets_path.strip() + '/'
    params = vars(args)

    gen_bloc_params = {}
    for ky, val in params.items():
        if( ky.startswith('bc_') ):
            gen_bloc_params[ky[3:]] = val
    
    merge_lst = [
        {
            'src': 'cresci-17',
            'new_class': 'bot',
            'old_classes': ['bot-fakefollower', 'bot-socialspam', 'bot-traditionspam']
        },
        {
            'src': 'zoher-organization',
            'new_class': 'human',
            'old_classes': ['celebrity', 'organization']    
        },
        {
            'src': 'celebrity-19',
            'new_class': 'human',
            'old_classes': ['celebrity', 'organization']    
        },
        {
            'src': 'astroturf',
            'new_class': 'bot',
            'old_classes': ['political_Bot']
        }
    ]

    src_maps = [
        ('kevin_feedback', 'botometer-feedback-19'),
        ('botwiki', 'botwiki-19'),
        ('caverlee', 'caverlee-11'),
        ('zoher-organization', 'celebrity-19'),
        ('rtbust', 'cresci-rtbust-19'),
        ('stock', 'cresci-stock-18'),
        ('midterm-2018', 'midterm-18'),
        ('josh_political', 'political-bots-19'),
        ('pronbots', 'pronbots-19'),
        ('varol-icwsm', 'varol-17'),
        ('gregory_purchased', 'vendor-purchased-19'),
        ('verified', 'verified-19')
    ]

    if( args.task == 'pca_general' and len(args.tweets_files) > 1 ):
        print('\n\ttask is pca_general, selecting first source since multiple were supplied.')
        args.tweets_files = [ args.tweets_files[0] ]

    all_datasets = get_bloc_for_tweets( args.tweets_files, args.tweets_path, gen_bloc_params, max_users=args.max_users, min_tweets=args.min_tweets, max_tweets=args.max_tweets, src_maps=src_maps )

    for src in all_datasets:
        print('src:', src)
        for clss, tweets in all_datasets[src].items():
            print('\tclss:', clss, len(tweets))

    
    
    if( args.no_merge is False ):
        merge_srcs( all_datasets, merge_lst, args.max_users )
        

    rename_cols( all_datasets, src_maps )
    add_more_details( all_datasets, 'sf-influenced' in args.evaluate_models )#must call this after merge_srcs and rename_cols
    

    if( 'sf-influenced' in args.evaluate_models ):
        print('\nDNA Influenced is on, removing action_content_syntactic from args.bc_bloc_alphabets')
        args.bc_bloc_alphabets.remove('action_content_syntactic')
    
    
    if( args.task == 'evaluate' ):
        all_datasets = flatten_dataset_shuffle( all_datasets )

    run_tasks(all_datasets, args)

if __name__ == "__main__":
    main()
