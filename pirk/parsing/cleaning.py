# extract x and y values for fitting using baseline_begin_time and baseline_end_time obtained through visual inspection
import numpy as np

from pirk.parsing.loader import parse_indices, parse_array
from pirk.utils.helpers import find_closest_index


def prep_traces_for_fitting(combined_df, index,
                            x_column_name='trace_time',
                            y_column_name='trace',
                            baseline_begin_time=0.35,
                            baseline_end_time=0.38):
    """
    Prepare ECS traces for fitting by selecting the dirk period, baseline-correcting
    the signal, and identifying pirk points.

    Parameters:
        combined_df (pd.DataFrame): DataFrame containing time and signal traces,
                                    as well as metadata like 'pps' and 'pirk_indexes'.
        index (int): Index of the trace to process from the DataFrame.
        x_column_name (str): Column name for the time trace. Default is '520_time'.
        y_column_name (str): Column name for the signal trace. Default is '520_calc'.
        baseline_begin_time (float): Start time (in seconds) for the baseline window.
        baseline_end_time (float): End time (in seconds) for the baseline window.

    Returns:
        trace_x (np.ndarray): Time values for the trimmed and baseline-aligned trace.
        trace_y (np.ndarray): Baseline-corrected signal trace.
        pirk_points (list of float): Time points corresponding to pirk stimulus onsets.
        dirk_point_indexes (list of int): Index positions of the pirk points relative to the trimmed trace.

    Notes:
        - Baseline is computed as the mean value between `baseline_begin_time` and `baseline_end_time`.
        - If 'pps' (pre-pulse points) is empty, fallback is to use 'pirk_indexes' for stimulation points.
        - Returned y-values are scaled by 1000.
    """

    b, e = parse_indices(combined_df['dirk_indices'][index])
    trace_y = parse_array(combined_df[y_column_name][index])[b:e]
    trace_x = parse_array(combined_df[x_column_name][index])[b:e]
    trace_x = trace_x - trace_x[0]  # np.min(trace_x)

    # must be a better way of finding the baseline!
    bb = find_closest_index(trace_x, baseline_begin_time)
    be = find_closest_index(trace_x, baseline_end_time)

    baseline = np.mean(trace_y[bb:be])

    trace_y = trace_y - baseline  # calc_min #baseline #calc_min #baseline
    # trace_y = trace_y/np.max(trace_y)
    # If pre pulses were not used, dirk_point_indexes = [], pirk_points are then calculated from acitnic intensities
    pps = parse_array(combined_df['pirk_points'][index])

    dirk_point_indexes = [i - b for i in pps if i >= b and i < e]

    pirk_points = [trace_x[i] for i in dirk_point_indexes]

    return trace_x, trace_y, pirk_points, dirk_point_indexes


