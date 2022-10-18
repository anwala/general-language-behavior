import gzip
import sys
import pandas as pd
import numpy as np
from os import X_OK

from numpy.lib.function_base import diff

from sklearn.model_selection import cross_val_score, cross_val_predict, StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from statistics import mean

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

def get_train_test_split(ds, n_splits=5):
    train_test_split_indices = []
    skf = StratifiedKFold( n_splits=n_splits, shuffle=True )

    for train_index, test_index in skf.split(ds, y):
        train_test_split_indices.append( (train_index, test_index) )

    return train_test_split_indices

def eval_ml_model(model, train_ds, correct_labels, train_test_split_indices):
    
    scores_f1 = cross_val_score(model, train_ds, correct_labels, cv=train_test_split_indices, scoring="f1")
    scores_recall = cross_val_score(model, train_ds, correct_labels, cv=train_test_split_indices, scoring="recall")
    scores_precision = cross_val_score(model, train_ds, correct_labels, cv=train_test_split_indices, scoring="precision")

    return {
        'f1-score': scores_f1.mean(),
        'recall': scores_recall.mean(),
        'precision': scores_precision.mean()
    }

def write_train_test_splits(feature_df, train_test_split_indices, outfilename):
    
    out_train_test_split = gzip.open(outfilename, 'wt')
    
    for train_index, test_index in train_test_split_indices:

        train_index = ','.join([ str(feature_df['userID'][indx]) for indx in train_index ])
        test_index = ','.join([ str(feature_df['userID'][indx]) for indx in test_index ])
        out_train_test_split.write(f'{train_index} ** {test_index}\n')
    
    out_train_test_split.close()

def fmt_df(feature_df):

    print('feature_df:')
    print(feature_df)

    bot_accounts   = feature_df[feature_df.label == 1]
    human_accounts = feature_df[feature_df.label == 0]

    print('bot_accounts.shape:', bot_accounts.shape)
    print('human_accounts.shape:', human_accounts.shape)
    print()

    min_class_count = min( bot_accounts.shape[0], human_accounts.shape[0] )
    bot_accounts = bot_accounts.head(min_class_count)
    human_accounts = human_accounts.head(min_class_count)

    feature_df = pd.concat([bot_accounts, human_accounts], ignore_index=True)
    feature_df = feature_df.sample(frac=1)

    
    total_bots = feature_df[feature_df.label == 1].shape[0]
    total_humans = feature_df[feature_df.label == 0].shape[0]
    print('total_bots:', total_bots)
    print('total_humans:', total_humans)
    print()

    return feature_df

features_path = sys.argv[1]
bloc_model = sys.argv[2]
out_path = sys.argv[-1]

print("Start to load the features")
feature_df = pd.read_csv(features_path)

print(f"Shuffle the features of {len(feature_df)} samples")
feature_df = feature_df.sample(frac=1)
feature_df = fmt_df(feature_df)


print("Start to prepare the X and y")
all_cols_list = feature_df.columns
all_cols = set(all_cols_list)

tfidf_cols = set(list(filter(lambda x: x.startswith("tfidf"), all_cols_list)))
other_cols = set(["user_id", "userID", "label"])
botometer_cols = all_cols - tfidf_cols - other_cols

botometer_cols_df = pd.DataFrame(botometer_cols, columns=["feature_name"])
botometer_cols_df["feature_type"] = botometer_cols_df.feature_name.apply(lambda x: x.split("_")[0])
y = feature_df["label"]

print(f"TFIDF features: {len(tfidf_cols)}; botometer features: {len(botometer_cols)}")
print("Start to evaluate the models")

# just bloc features
X_bloc = feature_df[list(tfidf_cols)]
train_test_split_indices = get_train_test_split(X_bloc)

different_combo_performance = []

#for boto_feature_type in ["content", "sentiment", "friend", "network", "user", "temporal", "all"]:
for boto_feature_type in ["all"]:
    for combo in [True, False]:

        if boto_feature_type == "all":
            temp_cols = set(botometer_cols_df.feature_name)
        else:
            temp_cols = set(
                botometer_cols_df.query(
                    f'feature_type == "{boto_feature_type}"'
                ).feature_name
            )

        if combo:
            temp_X = feature_df[list(temp_cols) + list(tfidf_cols)]
        else:
            temp_X = feature_df[temp_cols]

        rf_model = RandomForestClassifier(n_estimators=100)
        eval_report = eval_ml_model(rf_model, temp_X, y, train_test_split_indices)

        different_combo_performance.append(
            [
                boto_feature_type + "_bloc" if combo else boto_feature_type,
                eval_report['f1-score'], 
                eval_report['recall'], 
                eval_report['precision'],
                temp_X.shape[1],
            ]
        )
        print("Worked on {}, features: {}, if combo {} F1: {}".format(boto_feature_type, temp_X.shape[1], combo, eval_report['f1-score']))


# just bloc features
rf_model = RandomForestClassifier(n_estimators=100)
eval_report = eval_ml_model(rf_model, X_bloc, y, train_test_split_indices)

different_combo_performance.append(["bloc", eval_report['f1-score'], eval_report['recall'], eval_report['precision'], X_bloc.shape[1]])
print( "Worked on bloc, features: {} F1: {}".format(X_bloc.shape[1], eval_report['f1-score']) )
print()

different_combo_performance_df = pd.DataFrame(different_combo_performance, columns=["botometer_feature_category", "f1", "recall", "precision", "n_features"])
different_combo_performance_df["bloc_model"] = bloc_model
different_combo_performance_df.to_csv(out_path, index=None)


write_train_test_splits(feature_df, train_test_split_indices, out_path + '_cv_splits.gz')
