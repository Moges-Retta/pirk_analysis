import numpy as np
from matplotlib import cm

from pirk.parsing.loader import parse_array, parse_indices
from scipy.stats import linregress
import matplotlib.pyplot as plt

from pirk.names import DIRK_INDICES_COLUMN, TRACE_COLUMN,TIME_COLUMN


def find_predirk_baseline(combined_df, index, number_baseline_points=10):
    """ Find the baseline before the Dirk protocol in the experiment.
    Note: The Dirk protocol is defined by the actinic intensity that is set to the value of the Dirk parameter.
    It is assumed that the Dirk protocol is the only one with this intensity. If there are multiple Dirk intervals, the first beginning point will be the start of the first, and the ending point will be the last of the final.

        """

    dirk_points = parse_array(combined_df[DIRK_INDICES_COLUMN][index])

    dirk_begin = np.min(dirk_points)
    dirk_end = np.max(dirk_points)

    return dirk_begin - number_baseline_points, dirk_begin


def find_steady_state_pirk_amplitudes(combined_df, index, dirk_par=0, number_baseline_points=10, plot_it=False):
    """ Find the amplitude of the steady state PIRK signal in the experiment.
    Note: The Dirk protocol is defined by the actinic intensity that is set to the value of the Dirk parameter.
    This assumes that the Dirk protocol is the only one with this intensity. If there are multiple Dirk intervals, the first beginning point will be the start of the first, and the ending point will be the last of the final.
    This also assumes that there is one PIRK just before the inset of the DIRK.
    The baseline is calculated as the average of the last number_baseline_points before the Dirk protocol.
    The amplitude is calculated as the difference between the steady state PIRK signal and the baseline.

    input:
        exp_df: combined_df
        index: int, index of the experiment in the dataframe
        dirk_par: int, the value of the Dirk parameter that is used to define the Dirk protocol
        number_baseline_points: int, the number of points to use for the baseline calculation
        plot_it: bool, if True, plot the results

        """
    b, e = parse_indices(combined_df[DIRK_INDICES_COLUMN][index])
    trace_y = parse_array(combined_df[TRACE_COLUMN][index])[b:e]
    trace_x =  parse_array(combined_df[TIME_COLUMN][index])[b:e]

    base_b, base_e = find_predirk_baseline(combined_df, index)
    baseline_x = trace_x[base_b: base_e - 1]
    baseline_y = trace_y[base_b: base_e - 1]

    fitlin = linregress(baseline_x, baseline_y)

    steady_state_pirk_measurement_x = trace_x[base_e+1]
    steady_state_pirk_measurement = trace_y[base_e+1]

    # if fitlin.slope <0:
    # print(fitlin, fitlin.slope, fitlin.intercept)

    steady_state_pirk_baseline_fit = fitlin.slope * trace_x[base_b: base_e] + fitlin.intercept
    steady_state_pirk_baseline_fit_offset = steady_state_pirk_baseline_fit[-1]
    steady_state_pirk_baseline_fit_line = fitlin.slope * trace_x[base_b: base_e] + fitlin.intercept

    steady_state_pirk_amplitude = steady_state_pirk_measurement - steady_state_pirk_baseline_fit_line[-1]

    if plot_it:
        plt.figure()
        plt.plot(trace_x[b: b + 20], trace_y[b: b + 20], color='blue')

        plt.plot(trace_x[base_b: base_e], trace_y[base_b: base_e], color='yellow', label='baseline trace')
        plt.plot(trace_x[base_b: base_e], steady_state_pirk_baseline_fit_line, color='green', label='linear fit')
        plt.scatter(steady_state_pirk_measurement_x, steady_state_pirk_measurement, color='red', label='ss last point')

        # plt.plot(combined_df['520_time'][index][base_b : base_e], )
        plt.legend()
        plt.show()
    return steady_state_pirk_measurement_x, steady_state_pirk_amplitude