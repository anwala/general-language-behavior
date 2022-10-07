import pandas as pd
import sys

boto_features_path = sys.argv[1]
tfidf_path = sys.argv[2]

out_path = sys.argv[-1]

print("Start to load features")
feature_df = pd.read_csv(boto_features_path)

print("Start to load tfidf")
tfidf_df = pd.read_csv(tfidf_path)

print("Start to merge the data")
df = feature_df.merge(tfidf_df, left_on="userID", right_on="user_id")
df.to_csv(out_path, index=None)
