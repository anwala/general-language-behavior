import os
import numpy as np
import pandas as pd
import sys

from glcr import longest_common_subsequence
from digitaldna.lcs import LongestCommonSubsequence
from subprocess import check_output

from sklearn.metrics import classification_report
from sklearn.metrics import matthews_corrcoef
from statistics import mean

def generic_error_info(slug=''):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    
    err_msg = fname + ', ' + str(exc_tb.tb_lineno)  + ', ' + str(sys.exc_info())
    print(err_msg + slug)

    return err_msg

def unicode_to_ascii(array):
    def f(item):
        return str(item) + '\0'

    def v(x):
        return np.vectorize(f)(x)

    return v(array).astype('S')

def get_lcs_length_for_cut(lcs_mat_csv_file, cut):
    
    lcs_thresholds = []
    lcs_mat = pd.read_csv(lcs_mat_csv_file)


    for i in range( len(lcs_mat['num_texts']) ):

        num_accnt = lcs_mat['num_texts'][i]
        lcs_len = lcs_mat['length'][i]

        if( num_accnt == cut ):
            lcs_thresholds.append(lcs_len)

        if( num_accnt > cut ):
            break

    print('cut:', cut)
    print('lcs_thresholds:', lcs_thresholds)
    print()
    if( len(lcs_thresholds) == 0 ):
        lcs_thresholds = 0
    else:
        lcs_thresholds = mean(lcs_thresholds)
    
    return lcs_thresholds

def train_twitter_dna_model(t_dna, glcr_filename, df, offset, actu_labels=[]):

    max_mcc = -1
    max_mcc_lcs_threshold = 0

    est = LongestCommonSubsequence(in_path='', out_path=glcr_filename, overwrite=False, threshold=0, window=10, verbosity=3)
    est.fit(t_dna)

    print('train_twitter_dna_model() - start')
    t_dna_len = len(t_dna)
    for cut in range(offset+5, t_dna_len, offset):
        
        #est = LongestCommonSubsequence(in_path='', out_path=glcr_filename, overwrite=False, threshold=cut, window=10, verbosity=3)
        #pred_labels = est.fit_predict(t_dna)
        #lcs_threshold = get_lcs_length_for_cut( f'{glcr_filename}.mat', est.cut_ )

        est.threshold = cut
        pred_labels = est.predict(t_dna)
        lcs_threshold = get_lcs_length_for_cut( f'{glcr_filename}.mat', est.cut_ )

        #print(f'\t{cut} of {t_dna_len}')
        #print('\tlcs_threshold:', lcs_threshold)
        if( lcs_threshold == 0 ):
            break
    
        try:
            mcc = matthews_corrcoef(actu_labels, pred_labels)
        except:
            generic_error_info()
            continue
        #print('\tmcc:', mcc)

        if( mcc > max_mcc ):
            max_mcc = mcc
            max_mcc_lcs_threshold = lcs_threshold
        

    print('train_twitter_dna_model() - end\n')
    print('max_mcc:', max_mcc)
    print('max_mcc_lcs_threshold', max_mcc_lcs_threshold)


    if( df is not None ):
        df['pred_bot'] = y
        df.to_csv(f'{glcr_filename}_pred.csv')
        
    #lcs_est = est.plot_LCS()
    #lcs_est.savefig(f'{glcr_filename}_lcs_plt.png')
    #lcs_est.clf()

    #lcs_est = est.plot_LCS_log()
    #lcs_est.savefig(f'{glcr_filename}_lcs_plt_log.png')
    #lcs_est.clf()
    
    return max_mcc_lcs_threshold

def train_twitter_dna_model_for_threshold(t_dna, glcr_filename, df, threshold='auto'):

    est = LongestCommonSubsequence(in_path='', out_path=glcr_filename, overwrite=False, threshold=threshold, window=10, verbosity=3)
    y = est.fit_predict(t_dna)
    lcs_threshold = get_lcs_length_for_cut( f'{glcr_filename}.mat', est.cut_ )
    
    print('lcs_threshold (LCS length):', lcs_threshold, 'for cut:', est.cut_ )
    print('y', y)

    if( df is not None ):
        df['pred_bot'] = y
        df.to_csv(f'{glcr_filename}_pred.csv')

    
    lcs_est = est.plot_LCS()
    lcs_est.savefig(f'{glcr_filename}_lcs_plt.png')
    lcs_est.clf()

    #lcs_est = est.plot_LCS_log()
    #lcs_est.savefig(f'{glcr_filename}_lcs_plt_log.png')
    #lcs_est.clf()
    
    

    return lcs_threshold

def train_test_twitter_dna_model( pos_neg_class, training_set, test_set, start_offset, model_files_path='./TwitterDNA_Model_Files/'):

    model_files_path = model_files_path.strip()
    model_files_path = model_files_path if model_files_path.endswith('/') is True else model_files_path + '/'
    
    try:
        os.makedirs(model_files_path, exist_ok=True)
    except:
        generic_error_info()
        return {}

    print('\ntrain_test_twitter_dna_model():')
    print('\ttraining_set.len:', len(training_set))
    print('\ttest_set.len:', len(test_set))
    '''
        Steps: 
        1. Fit and predict training set to get a cut (x-axis in LCS Curve)
        2. Use cut to find LCS length (y-axis in LCS Curve) in training set. Let's call this value: Training_LCS_length_threshold
        3. Draw LCS curve for test set
        4. Use Training_LCS_length_threshold (y-axis) to find place (x-axis) to cut test set
        5. After cutting the test set. We can use *.mat to label accounts that are bots as those having subsequences that are >= Training_LCS_length_threshold
    '''
    
    glcr_file = f'{model_files_path}twt_dna_model'
    
    #Step 1 - 4
    #train model - start
    #this call would genrated: f'{glcr_file}.mat'
    
    sf_train_docs = []
    actu_labels = []
    for d in training_set:
        sf_train_docs.append(d['text'])
        actu_labels.append(d['class'] == 'bot')

    lcs_threshold = train_twitter_dna_model( sf_train_docs, glcr_file, df=None, offset=start_offset, actu_labels=actu_labels )

    #from bloc.util import dumpJsonToFile
    #dumpJsonToFile('sample_tdna_training_data_v2.json', training_set)
    #train model - end

    sf_test_docs = [ d['text'] for d in test_set ]
    try:
        longest_common_subsequence( unicode_to_ascii(sf_test_docs), '', f'{glcr_file}_test', 3 )
        test_df = pd.read_csv(f'{glcr_file}_test.mat')
    except:
        generic_error_info()
        return {}

    print('\ttesting start')

    for i in range( len(test_set) ):
        test_set[i]['prediction_label'] = pos_neg_class['non_bot_class']

    seq_history = set()
    for i in range( len(test_df.index) ):
        
        lcs = test_df['subsequence'][i]
        num_users = test_df['num_texts'][i]

        if( lcs in seq_history ):
            continue
        
        #len(lcs) of all bots >= lcs_threshold
        if( len(lcs) < lcs_threshold ):
            break
        
        seq_history.add(lcs)
        for j in range( len(test_set) ):
            #all accounts that contain lcs as substring are bots since it longer than lcs_threshold
            if( test_set[j]['text'].find(lcs) != -1 ):
                #Step 5. After cutting the test set. We can use *.mat to label accounts that are bots as those having subsequences that are >= Training_LCS_length_threshold
                test_set[j]['prediction_label'] = pos_neg_class['bot_class']
    
    
    all_classes = [pos_neg_class['non_bot_class'], pos_neg_class['bot_class']]
    all_classes.sort()
    conf_mat = np.zeros( (len(all_classes), len(all_classes)) )

    y_pred = []
    y_true = []
    class_rep = {}
    for t in test_set:
        
        y_pred.append( t['prediction_label'] )
        y_true.append( t['class'] )

        pred_i = all_classes.index( t['prediction_label'] )
        actu_i = all_classes.index( t['class'] )
        conf_mat[pred_i, actu_i] += 1


    if( len(y_pred) != 0 and len(y_true) != 0 ):

        class_rep['classification_report'] = classification_report(y_true, y_pred, output_dict=True, target_names=all_classes)
        class_rep['all_classes'] = all_classes
        class_rep['confusion_matrix'] = conf_mat
    
    print('\ttesting end')

    return class_rep