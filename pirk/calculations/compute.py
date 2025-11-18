import numpy as np
from matplotlib import cm

from pirk.parsing.loader import parse_array, parse_indices
from scipy.stats import linregress
import matplotlib.pyplot as plt


def find_predirk_baseline(combined_df, index, dirk_par=0, number_baseline_points=10):
    """ Find the baseline before the Dirk protocol in the experiment.
    Note: The Dirk protocol is defined by the actinic intensity that is set to the value of the Dirk parameter.
    It is assumed that the Dirk protocol is the only one with this intensity. If there are multiple Dirk intervals, the first beginning point will be the start of the first, and the ending point will be the last of the final.

        """
    # actinic_intensities = ast.literal_eval(combined_df['actinic_intensity_per_point'][index])
    # actinic = list(zip(actinic_intensities, list(range(0, len(actinic_intensities)))))
    # dirk_points = [a[1] for a in actinic if a[0] == 0]

    dirk_points = parse_array(combined_df['dirk_indices_updated'][index])

    dirk_begin = np.min(dirk_points)
    dirk_end = np.max(dirk_points)

    return (dirk_begin - number_baseline_points, dirk_begin)


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

    b, e = parse_indices(combined_df['dirk_indices_updated'][index])
    trace_y = parse_array(combined_df['trace_replaced'][index])
    trace_x = parse_array(combined_df['trace_time'][index])

    base_b, base_e = find_predirk_baseline(combined_df, index)
    baseline_x = trace_x[base_b: base_e - 1]
    baseline_y = trace_y[base_b: base_e - 1]

    fitlin = linregress(baseline_x, baseline_y)

    steady_state_pirk_measurement_x = trace_x[base_e]
    steady_state_pirk_measurement = trace_y[base_e]

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


def calculate_PSI(trace, trace_indices):
    PSI_ss_beg = trace_indices.get('PSI_ss_beg')  # beginning of the trace for P700 steady-state
    PSI_ss_end = trace_indices.get('PSI_ss_end')  # end of the trace for P700 steady-state
    PSI_sat1_beg = trace_indices.get('PSI_sat1_beg')  # beginning of the trace for P700 first saturation pulse
    PSI_sat1_end = trace_indices.get('PSI_sat1_end')  # end of the trace for P700 first saturation pulse
    PSI_dark_beg = trace_indices.get('PSI_dark_beg')  # beginning of the trace for P700 steady-state
    PSI_dark_end = trace_indices.get('PSI_dark_end')  # end of the trace for P700 steady-state
    PSI_sat2_beg = trace_indices.get('PSI_sat2_beg')  # beginning of the trace for P700 second saturation pulse
    PSI_sat2_end = trace_indices.get('PSI_sat2_end')  # end of the trace for P700 second saturation pulse

    # transform trace using average trace values of light adapted leaf, photorides 2 protocol
    trace_Dark = np.mean(trace[PSI_dark_beg:PSI_dark_end])

    PSI_data_absorbance = []
    for i in trace:
        PSI_data_absorbance.append(np.log10(trace_Dark / i))

    PSI_ss = np.mean(PSI_data_absorbance[PSI_ss_beg:PSI_ss_end])

    PSI_sat1 = np.mean(PSI_data_absorbance[PSI_sat1_beg:PSI_sat1_end])

    PSI_sat2 = np.mean(PSI_data_absorbance[PSI_sat2_beg:PSI_sat2_end])

    PSI_ss = 1000 * np.mean(PSI_data_absorbance[PSI_ss_beg:PSI_ss_end])

    PSI_sat1_vals = PSI_data_absorbance[PSI_sat1_beg:PSI_sat1_end]
    PSI_sat1_vals.sort()  # sort the saturating light values from low to high
    length_of_sat1 = PSI_sat1_end - PSI_sat1_beg
    top_20_percent = int(length_of_sat1 * 0.8)
    PSI_sat1 = 1000 * np.mean(
        PSI_sat1_vals[top_20_percent:length_of_sat1])  # take the top 20% largest values and average them

    PSI_sat2_vals = PSI_data_absorbance[PSI_sat2_beg:PSI_sat2_end]
    PSI_sat2_vals.sort()  # sort the saturating light values from low to high
    length_of_sat2 = PSI_sat2_end - PSI_sat2_beg
    top_20_percent = int(length_of_sat2 * 0.8)
    PSI_sat2 = 1000 * np.mean(
        PSI_sat2_vals[top_20_percent:length_of_sat2])  # take the top 20% largest values and average them

    PSI_ox = PSI_ss / PSI_sat2
    PSI_act = PSI_sat2
    PSI_open = (PSI_sat1 - PSI_ss) / PSI_sat2
    PSI_or = 1 - PSI_sat1 / PSI_sat2

    return [PSI_ox, PSI_act, PSI_open, PSI_or]


def calculate_ps1_all(combined_df, index, trace_indices):
    trace = parse_array(combined_df['trace'][index])
    [PSI_ox, PSI_act, PSI_open, PSI_or] = calculate_PSI(trace, trace_indices)

    add_new_cols = True
    if add_new_cols:
        combined_df.at[index, 'PSI_ox'] = PSI_ox
        combined_df.at[index, 'PSI_act'] = PSI_act
        combined_df.at[index, 'PSI_open'] = PSI_open
        combined_df.at[index, 'PSI_or'] = PSI_or

    print("PS1 Active Centers", np.round(PSI_act, 3))
    print("PS1 Open Centers", np.round(PSI_open, 3))
    print("PS1 Over Reduced Centers", np.round(PSI_or, 3))
    print("PS1 Oxidized Centers", np.round(PSI_ox, 3))

    replicate = combined_df['replicate'][index]
    genotype = combined_df['genotype'][index]
    light = combined_df['light_intensity'][index]
    time = np.linspace(0, len(trace), len(trace))
    colors = cm.get_cmap('tab10', replicate)  # Or 'viridis', 'plasma', 'rainbow', etc.
    plt.plot(time, trace, color=colors(int(replicate)), label=replicate)
    plt.title(f'Genotype : {genotype} Light :{light}')
    plt.show()



