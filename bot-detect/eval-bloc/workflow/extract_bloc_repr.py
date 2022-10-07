"""
This script extracts the bloc representation of the twitter users
"""
from bloc.generator import add_bloc_sequences
import sys
import gzip
import json
import traceback

tweet_path = sys.argv[1]
out_path = sys.argv[-1]

tweets_bloc_strs = []
with gzip.open(tweet_path) as f:
    for line in f:
        try:
            user_id, tweets_str = line.strip().split(b"\t")
            print(f"Working on {user_id}")
            tweets = json.loads(tweets_str)
            authored_tweets = []
            for tweet in tweets:
                if int(tweet["user"]["id_str"]) == int(user_id):
                    authored_tweets.append(tweet)
            tweets_bloc = add_bloc_sequences(tweets)
            tweets_bloc_strs.append(json.dumps(tweets_bloc))
        except Exception as e:
            print(traceback.format_exc())

tweets_bloc_str = "\n".join(tweets_bloc_strs)
with gzip.open(out_path, "wb") as f:
    f.write(tweets_bloc_str.encode("utf-8"))
