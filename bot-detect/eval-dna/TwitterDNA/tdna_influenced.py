import itertools
import os
import numpy as np
import sys

from math import log2
from sklearn.metrics import classification_report

def generic_error_info(slug=''):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    
    err_msg = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
    print(err_msg + slug)

    return err_msg

def partition_lst(payload, chunk_size):
    chunked_indx = [
        {
            'chunk_size': len(payload[i:i+chunk_size]),
            'range': {'start': payload[i:i+chunk_size][0], 'end': payload[i:i+chunk_size][-1] + 1}
        } 
        for i in range(0, len(payload), chunk_size)
    ]
    return chunked_indx

def kl_divergence(p, q):
    return sum(p[i] * log2(p[i]/q[i]) for i in range(len(p)))

def get_valid_dna_inf_str(dna_inf_text):
    return ''.join([ s for s in dna_inf_text.strip() if s in ['A', 'T', 'G', 'C'] ])

def calc_prob_dist_of_dna(dna_inf_text):

    weights = {'T': 0.2, 'A': 0.4, 'G': 0.6, 'C': 0.8}
    dna_inf_weights = [ weights[s] for s in dna_inf_text if s in ['A', 'T', 'G', 'C'] ]
    
    if( len(dna_inf_text) < 3 ):
        return None
    
    probs = []
    n = len(dna_inf_text)
    denom = ((0.5*n)*(n+1)) - sum(dna_inf_weights)
    
    for i in range(n):
        
        β_i = dna_inf_weights[i]
        α_i = i + 1
        probs.append( (α_i - β_i)/denom )
    
    return probs

def calc_rel_entropy_dist(a_dna, b_dna):

    def get_subsequences(dna_str, sub_len):
        return [ dna_str[i:i+sub_len] for i in range(0, len(dna_str) - sub_len + 1) ]

    dna_pair = [ get_valid_dna_inf_str(a_dna), get_valid_dna_inf_str(b_dna) ]
    dna_pair_len = [ len(dna_pair[0]), len(dna_pair[1]) ]

    if( dna_pair_len[0] == dna_pair_len[1] ):
        p = calc_prob_dist_of_dna(dna_pair[0])
        q = calc_prob_dist_of_dna(dna_pair[1])
        return (kl_divergence(p, q) + kl_divergence(q, p))/2
    else:
        
        min_length, max_indx = (dna_pair_len[0], 1) if dna_pair_len[0] < dna_pair_len[1] else (dna_pair_len[1], 0)
        subseqs = get_subsequences( dna_pair[max_indx], min_length )
        avg_prob_dist = np.zeros(min_length)
        
        for s in subseqs:
            avg_prob_dist += np.array( calc_prob_dist_of_dna(s) )
        
        min_indx = 1 - max_indx
        p = avg_prob_dist/len(subseqs)
        q = calc_prob_dist_of_dna(dna_pair[min_indx])
        
        return (kl_divergence(p, q) + kl_divergence(q, p))/2

def train_test_twitter_dna_influenced_model(pos_neg_class, training_set, test_set):

    '''
    Steps: 
    1. Calculate probablity dist for all users (training_set and test_set)
    2. Decision threshold = Max relative entropy similarity across all bot pairs in training_set
    3. For account pairs u_i, u_j in test_set, if d(u_i, u_j) <= Decision threshold, declare both as bots
    '''

    for i in range( len(test_set) ):
        test_set[i]['prediction_label'] = pos_neg_class['non_bot_class']
   
    #train model - start
    
    bot_decision_threshold = 0
    pairs = [ bot[0] for bot in enumerate(training_set) if bot[1]['class'] == 'bot' ]
    pairs = list( itertools.combinations(pairs, 2) )

    #get partition of 50 chunks
    bot_pair_partitions = partition_lst(list(range(len(pairs))), 50)

    for b in bot_pair_partitions:
        
        mean_ent_dist = 0
        ent_dist_count = 0
        for i in range(b['range']['start'], b['range']['end']):
            
            fst_indx, sec_indx = pairs[i]
            u = training_set[fst_indx]
            v = training_set[sec_indx]

            if( len(u['text']) < 3 or len(v['text']) < 3 ):
                continue
            
            ent_dist = calc_rel_entropy_dist( u['text'], v['text'] )
            mean_ent_dist += ent_dist
            ent_dist_count += 1

        mean_ent_dist = 0 if ent_dist_count == 0 else mean_ent_dist/ent_dist_count
        
        if( mean_ent_dist > bot_decision_threshold ):
            bot_decision_threshold = mean_ent_dist      
    #train model - end
    


    #predict bots - start
    pairs = list( range( len(test_set) ) )
    pairs = list( itertools.combinations(pairs, 2) )
    
    for fst_indx, sec_indx in pairs:
        
        fst_dna = test_set[fst_indx]['text']
        sec_dna = test_set[sec_indx]['text']
        
        if( len(fst_dna) < 3 or len(sec_dna) < 3 ):
            test_set[fst_indx]['prediction_label'] = None
            test_set[sec_indx]['prediction_label'] = None
            continue

        rel_ent_dist = calc_rel_entropy_dist(fst_dna,sec_dna)
        if( rel_ent_dist <= bot_decision_threshold ):
            test_set[fst_indx]['prediction_label'] = pos_neg_class['bot_class']
            test_set[sec_indx]['prediction_label'] = pos_neg_class['bot_class']
    #predict bots - end
   
    
    all_classes = [pos_neg_class['non_bot_class'], pos_neg_class['bot_class']]
    all_classes.sort()
    conf_mat = np.zeros( (len(all_classes), len(all_classes)) )

    y_pred = []
    y_true = []
    class_rep = {}
    for t in test_set:
        
        if( t['prediction_label'] is None ):
            continue

        y_pred.append( t['prediction_label'] )
        y_true.append( t['class'] )

        pred_i = all_classes.index( t['prediction_label'] )
        actu_i = all_classes.index( t['class'] )
        conf_mat[pred_i, actu_i] += 1


    if( len(y_pred) != 0 and len(y_true) != 0 ):

        class_rep['classification_report'] = classification_report(y_true, y_pred, output_dict=True, target_names=all_classes)
        class_rep['all_classes'] = all_classes
        class_rep['confusion_matrix'] = conf_mat
    
    return class_rep