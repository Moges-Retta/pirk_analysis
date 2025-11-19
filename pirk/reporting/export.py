import os

import numpy as np
import os
import pandas as pd

def save_combined_df(df, filename, path, file_format='pkl', overwrite=True):
    """
    Save a DataFrame to a specified path with optional format.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to save.
    filename : str
        Name of the file without extension.
    path : str
        Directory path where the file will be saved.
    file_format : str, optional
        File format: 'pkl' (pickle) or 'csv'. Default is 'pkl'.
    overwrite : bool, optional
        Whether to overwrite existing file. Default is True.

    Returns
    -------
    full_path : str
        Full path of the saved file.
    """
    # Ensure directory exists
    os.makedirs(path, exist_ok=True)

    ext = file_format.lower()
    if ext not in ['pkl', 'csv']:
        raise ValueError("file_format must be 'pkl' or 'csv'")

    full_path = os.path.join(path, f"{filename}.{ext}")

    if not overwrite and os.path.exists(full_path):
        raise FileExistsError(f"File {full_path} already exists. Set overwrite=True to replace it.")

    if ext == 'pkl':
        df.to_pickle(full_path)
    elif ext == 'csv':
        df.to_csv(full_path, index=False)

    print(f"DataFrame saved to {full_path}")
    return full_path

