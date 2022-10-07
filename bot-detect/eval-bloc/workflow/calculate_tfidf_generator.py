"""
This script calculate the tfidf for all the users
"""
from bloc.tweet_generators import user_tweets_generator_0
from bloc.util import conv_tf_matrix_to_json_compliant
from bloc.util import get_bloc_variant_tf_matrix
import sys
import gzip
import json
import traceback

raw_tweet_paths = sys.argv[1:-2]
bloc_model = sys.argv[-2]
out_path = sys.argv[-1]

minimum_document_freq = 2
bloc_settings = {
    "m1": {
        "name": "m1: bigram",
        "ngram": 2,
        "token_pattern": "[^ |()*]",
        "bloc_variant": None,
        "bloc_alphabets": ["action", "content_syntactic"],
        "gen_rt_content": True,
        "sort_action_words": False,
    },
    "m2": {
        "name": "m2: word-basic",
        "ngram": 1,
        "token_pattern": "[^□⚀⚁⚂⚃⚄⚅ |()*]+|[□⚀⚁⚂⚃⚄⚅]",
        "bloc_variant": {
            "type": "folded_words",
            "fold_start_count": 4,
            "count_applies_to_all_char": False,
        },
        "bloc_alphabets": ["action", "content_syntactic"],
        "gen_rt_content": False,
        "sort_action_words": False,
    },
    "m3": {
        "name": "m3: word-content-with-pauses",
        "ngram": 1,
        "token_pattern": "[^□⚀⚁⚂⚃⚄⚅ |*]+|[□⚀⚁⚂⚃⚄⚅]",
        "bloc_variant": {
            "type": "folded_words",
            "fold_start_count": 4,
            "count_applies_to_all_char": False,
        },
        "bloc_alphabets": ["action", "content_syntactic_with_pauses"],
        "gen_rt_content": False,
        "sort_action_words": True,
    },
    "m4": {
        "name": "m4: word-action-content-session",
        "ngram": 1,
        "token_pattern": "[^□⚀⚁⚂⚃⚄⚅ |*]+|[□⚀⚁⚂⚃⚄⚅]",
        "bloc_variant": {
            "type": "folded_words",
            "fold_start_count": 4,
            "count_applies_to_all_char": False,
        },
        "bloc_alphabets": ["action_content_syntactic"],
        "gen_rt_content": False,
        "sort_action_words": True,
    },
    "m5": {
        "name": "m6: word-sort-action",
        "ngram": 1,
        "token_pattern": "[^□⚀⚁⚂⚃⚄⚅ |()*]+|[□⚀⚁⚂⚃⚄⚅]",
        "bloc_variant": {
            "type": "folded_words",
            "fold_start_count": 4,
            "count_applies_to_all_char": False,
        },
        "bloc_alphabets": ["action", "content_syntactic"],
        "gen_rt_content": False,
        "sort_action_words": True,
    },
    "m6": {
        "name": "m7: word-sort-action-gen-rt",
        "ngram": 1,
        "token_pattern": "[^□⚀⚁⚂⚃⚄⚅ |()*]+|[□⚀⚁⚂⚃⚄⚅]",
        "bloc_variant": {
            "type": "folded_words",
            "fold_start_count": 4,
            "count_applies_to_all_char": False,
        },
        "bloc_alphabets": ["action", "content_syntactic"],
        "gen_rt_content": True,
        "sort_action_words": True,
    },
}.get(bloc_model)

pos_id_mapping = {}
gen_bloc_params = {"bloc_alphabets": bloc_settings["bloc_alphabets"], "gen_rt_content": bloc_settings["gen_rt_content"], "sort_action_words": bloc_settings["sort_action_words"]}
input_files = raw_tweet_paths

doc_lst = user_tweets_generator_0(
    input_files, pos_id_mapping, rm_doc_text=True, gen_bloc_params=gen_bloc_params
)

tf_matrices = get_bloc_variant_tf_matrix(
    doc_lst,
    min_df=minimum_document_freq,
    ngram=bloc_settings["ngram"],
    token_pattern=bloc_settings["token_pattern"],
    bloc_variant=bloc_settings["bloc_variant"],
    pos_id_mapping=pos_id_mapping,
    keep_tf_matrix=False,
    tf_idf_norm='l2'
)

with gzip.open(out_path, "wb") as f:
    tf_matrices = conv_tf_matrix_to_json_compliant(tf_matrices)
    out_str = json.dumps(tf_matrices)
    f.write(out_str.encode("utf-8"))
