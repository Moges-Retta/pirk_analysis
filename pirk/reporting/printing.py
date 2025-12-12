from pirk.names import DEFAULT_OUTPUT_PATH
from pirk.reporting.tables import print_fit_table

def report_dirk_pirk_fit(combined_df, index, guess_dict, fit, pcov, trace_y, dirk_pirk_y):
    """
    Print fit summary table (or export CSV if needed).
    """
    print_fit_table(
        combined_df,
        index,
        guess_dict,
        fit,
        pcov,
        trace_y,
        dirk_pirk_y,
        export_csv=False,
        csv_path=None #DEFAULT_OUTPUT_PATH
    )

