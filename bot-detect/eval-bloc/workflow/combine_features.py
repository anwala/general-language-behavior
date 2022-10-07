"""
This file combine the botometer features
"""
import pandas as pd
import sys

feature_paths = sys.argv[1:-1]
out_path = sys.argv[-1]

raw_feature_dfs = []
for feature_path in feature_paths:
    temp_df = pd.read_csv(feature_path)
    raw_feature_dfs.append(temp_df)

usecols = raw_feature_dfs[0].columns
print(f"Keep {len(usecols)} columns")

feature_dfs = []
for df in raw_feature_dfs:
    temp_df = df[usecols]
    feature_dfs.append(temp_df)

feature_df = pd.concat(feature_dfs)

feature_df.drop_duplicates(subset=["userID"], inplace=True)

feature_df.to_csv(out_path, index=None)
