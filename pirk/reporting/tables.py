import os

import numpy as np
import pandas as pd

from pirk.names import GENOTYPE_COLUMN, TREATMENT_COLUMN, LABEL_COLUMN, REPLICATE_COLUMN, TREATMENT_NAME


def print_fit_table(combined_df, index, guess_dict, fit, pcov, trace_y, dirk_pirk_y, export_csv=False, csv_path=None):
    """
    Print a table of fitted parameters, standard errors, and 95% confidence intervals.
    Optionally, export the table to a CSV file.

    Parameters
    ----------
    combined_df : pd.DataFrame
        DataFrame containing metadata like genotype and replicate.
    index : int
        Index of the current trace.
    guess_dict : dict
        Dictionary of initial guess parameter names and values.
    fit : array-like
        Fitted parameter values.
    pcov : array-like
        Covariance matrix from the fitting.
    trace_y : array-like
        Original y-values.
    dirk_pirk_y : array-like
        Fitted y-values.
    export_csv : bool, optional
        Whether to export the table to CSV (default False).
    csv_path : str, optional
        Path to save the CSV file if export_csv is True.
    """
    perr = np.sqrt(np.diag(pcov))
    residuals = trace_y - dirk_pirk_y
    rmse = np.sqrt(np.mean(residuals ** 2))
    labels = list(guess_dict.keys())

    threshold = 0.5  # relative error threshold

    print(
        f"\nFitted Parameters and Standard Errors | index {index} : "
        f"{GENOTYPE_COLUMN}: {combined_df[GENOTYPE_COLUMN][index]} "
        f"{REPLICATE_COLUMN}: {combined_df[REPLICATE_COLUMN][index]} "
        f"{TREATMENT_NAME}: {combined_df[TREATMENT_COLUMN][index]}\n")
    print(f"RMSE: {rmse:.3f}")
    print(f"{'Parameter':35} {'Value':>10} {'Std. Error':>12} {'95% CI':>15}")
    print("-" * 85)

    table_data = []
    for label, val, err in zip(labels, fit, perr):
        rel_err = abs(err / val) if val != 0 else float('inf')
        ci_low = val - 1.96 * err
        ci_high = val + 1.96 * err

        color_start = '\033[91m' if rel_err > threshold or np.round(err, 3) == 0 else ''
        color_end = '\033[0m' if color_start else ''

        print(f"{color_start}{label:35} {val:10.3f} {err:12.3f} [{ci_low:7.3f}, {ci_high:7.3f}]{color_end}")

        table_data.append({
            'Parameter': label,
            'Value': val,
            'Std_Error': err,
            'CI_Lower': ci_low,
            'CI_Upper': ci_high
        })

    # Export table to CSV if requested
    if export_csv:
        # Ensure output path is a directory
        if csv_path is None:
            csv_path = f"fit_table_{combined_df[LABEL_COLUMN][index]}_index_{index}.csv"

        # If user passed a directory, generate a filename inside it
        if os.path.isdir(csv_path):
            csv_path = os.path.join(csv_path, f"fit_table_{combined_df[LABEL_COLUMN][index]}_index_{index}.csv")

        df_export = pd.DataFrame(table_data)
        df_export["RMSE"] = rmse

        df_export.to_csv(csv_path, index=False)
        print(f"\n✅ Fit table exported to {csv_path}")