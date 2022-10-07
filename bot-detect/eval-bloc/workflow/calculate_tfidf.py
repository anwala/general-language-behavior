"""
This script calculate the tfidf for all the users
"""
from bloc.util import get_bloc_doc_lst
from bloc.util import get_bloc_variant_tf_matrix
import sys
import gzip
import json
import traceback

bloc_paths = sys.argv[1:-2]
bloc_model = sys.argv[-2]
out_path = sys.argv[-1]

minimum_document_freq = 2
bloc_settings = {
    "m1": {
        "name": "m1: bigram",
        "ngram": 2,
        "token_pattern": "[^ |()*]",
        "bloc_variant": None,
        "dimensions": ["action", "content_syntactic"],
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
        "dimensions": ["action", "content_syntactic"],
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
        "dimensions": ["action", "content_syntactic_with_pauses"],
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
        "dimensions": ["action", "action_content_syntactic"],
    },
}.get(bloc_model)

print("Start to load bloc repr")
collection = []
for bloc_path in bloc_paths:
    print(f"Working on {bloc_path}")
    with gzip.open(bloc_path) as f:
        for line in f:
            bloc_repr = json.loads(line)
            collection.append(bloc_repr)

bloc_doc_lst = get_bloc_doc_lst(
    collection, bloc_settings["dimensions"], src="all", src_class="_"
)

print("Start to convert to TFIDF")
tf_matrices = get_bloc_variant_tf_matrix(
    bloc_doc_lst,
    min_df=minimum_document_freq,
    ngram=bloc_settings["ngram"],
    token_pattern=bloc_settings["token_pattern"],
    bloc_variant=bloc_settings["bloc_variant"],
)

with gzip.open(out_path, "wb") as f:
    out_str = json.dumps(tf_matrices)
    f.write(out_str.encode("utf-8"))
