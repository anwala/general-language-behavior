import sys
import pandas as pd

input_paths = sys.argv[1:-1]
out_path = sys.argv[-1]

print("Start to load tables")
dfs = []
for input_path in input_paths:
    print(f"Workign on {input_path}")
    temp_df = pd.read_csv(input_path)
    dfs.append(temp_df)

df = pd.concat(dfs)
print("Start to dump the results")
df.to_csv(out_path, index=None)
