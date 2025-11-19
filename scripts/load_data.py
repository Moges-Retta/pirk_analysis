import os

import pandas as pd


def load_combined_df(path,file_name):

    full_path = os.path.join(path, file_name)

    # Load DataFrame
    combined_df = pd.read_pickle(full_path)

    # Optional: print summary
    print(f"Loaded DataFrame with {len(combined_df)} rows and {len(combined_df.columns)} columns")
    return combined_df
