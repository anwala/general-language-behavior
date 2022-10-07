"""
This script extract the tfidf from the JSON objects and convert them into a table
"""
import pandas as pd
import sys
import gzip
import json
import traceback

input_path = sys.argv[1]
out_path = sys.argv[-1]

print("Start to load the raw file")
with gzip.open(input_path) as f:
    tfidf = json.load(f)

print("Start to extract TFIDF")
user_ids = []
tf_idf_vectors = []
for item in tfidf["tf_idf_matrix"]:
    tf_idf_vectors.append(item["tf_vector"])
    user_ids.append(item["user_id"])

print("Start to convert TFIDF into table")
tf_idf_df = pd.DataFrame(
    tf_idf_vectors,
    columns=[f"tfidf_{index}" for index in range(len(tf_idf_vectors[0]))],
)
tf_idf_df["user_id"] = user_ids

tf_idf_df.drop_duplicates(subset=["user_id"], inplace=True)
print(f"Got {len(tf_idf_df.columns)} tfidf features")

print("Start to dump the result")
tf_idf_df.to_csv(out_path, index=None)
