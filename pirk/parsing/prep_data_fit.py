# extract x and y values for fitting using baseline_begin_time and baseline_end_time obtained through visual inspection
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from pirk.parsing.loader import parse_indices, parse_array
from pirk.parsing.helpers import find_closest_index
from pirk.names import *


def prep_traces_for_fitting(combined_df, index):
    """
    Prepare ECS traces for fitting by selecting the dirk period, baseline-correcting
    the signal, and identifying pirk points.

    Parameters:
        combined_df (pd.DataFrame): DataFrame containing time and signal traces,
                                    as well as metadata like 'pps' and 'pirk_indexes'.
        index (int): Index of the trace to process from the DataFrame.

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

    b, e = parse_indices(combined_df[DIRK_INDICES_COLUMN][index])
    trace_y = parse_array(combined_df[TRACE_COLUMN][index])[b:e]
    trace_x =  parse_array(combined_df[TIME_COLUMN][index])[b:e]
    trace_x = trace_x - trace_x[0]  # np.min(trace_x)

    # must be a better way of finding the baseline!
    bb = find_closest_index(trace_x, BASELINE_BEGIN_TIME)
    be = find_closest_index(trace_x, BASELINE_END_TIME)

    baseline = np.mean(trace_y[bb:be])

    trace_y = trace_y - baseline  # calc_min #baseline #calc_min #baseline

    #  ECS and P700 PIRK need scaling for robust fitting
    trace_y = trace_y*1000 if combined_df.at[index,LABEL_COLUMN] in [LABEL_ECS,LABEL_P700] else trace_y

    # trace_y = trace_y/np.max(trace_y)
    # If pre pulses were not used, dirk_point_indexes = [], pirk_points are then calculated from light intensities
    pps = parse_array(combined_df[PIRK_POINTS_COLUMN][index])

    dirk_point_indexes = [i - b for i in pps if b <= i < e]
    pirk_points = [0] + [trace_x[i] for i in dirk_point_indexes]

    # trace_y_peak = [trace_y[0]] +[trace_y[i] for i in dirk_point_indexes]
    #
    # plt.figure()
    # plt.plot(trace_x,trace_y)
    # plt.plot(pirk_points,trace_y_peak,'o',color='red',label='prik points')
    # plt.xlabel('TIme (s)')
    # plt.show()
    return trace_x, trace_y, pirk_points, dirk_point_indexes


