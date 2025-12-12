import numpy as np
from matplotlib import cm, pyplot as plt

from pirk.parsing.loader import parse_array
from pirk.names import *

def _calculate_PSI(trace, trace_indices):
    PSI_ss_beg = trace_indices.get(PSI_SS_BEG)  # beginning of the trace for P700 steady-state
    PSI_ss_end = trace_indices.get(PSI_SS_END)  # end of the trace for P700 steady-state
    PSI_sat1_beg = trace_indices.get(PSI_SAT1_BEG)  # beginning of the trace for P700 first saturation pulse
    PSI_sat1_end = trace_indices.get(PSI_SAT1_END)  # end of the trace for P700 first saturation pulse
    PSI_dark_beg = trace_indices.get(PSI_DARK_BEG)  # beginning of the trace for P700 steady-state
    PSI_dark_end = trace_indices.get(PSI_DARK_END)  # end of the trace for P700 steady-state
    PSI_sat2_beg = trace_indices.get(PSI_SAT2_BEG)  # beginning of the trace for P700 second saturation pulse
    PSI_sat2_end = trace_indices.get(PSI_SAT2_END)  # end of the trace for P700 second saturation pulse

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


def calculate_ps1_all(combined_df, index, trace_indices,plot_all=True):
    trace = parse_array(combined_df[TRACE_COLUMN][index])
    [PSI_ox, PSI_act, PSI_open, PSI_or] = _calculate_PSI(trace, trace_indices)

    add_new_cols = True
    if add_new_cols:
        combined_df.at[index, PSI_OX] = PSI_ox
        combined_df.at[index, PSI_ACT] = PSI_act
        combined_df.at[index, PSI_OPEN] = PSI_open
        combined_df.at[index, PSI_OR] = PSI_or


    print("PS1 Active Centers", np.round(PSI_act, 3))
    print("PS1 Open Centers", np.round(PSI_open, 3))
    print("PS1 Over Reduced Centers", np.round(PSI_or, 3))
    print("PS1 Oxidized Centers", np.round(PSI_ox, 3))
    if plot_all:
        replicate = combined_df[REPLICATE_COLUMN][index]
        genotype = combined_df[GENOTYPE_COLUMN][index]
        light = combined_df[TREATMENT_COLUMN][index]
        time = np.linspace(0, len(trace), len(trace))
        colors = cm.get_cmap('tab10', replicate)  # Or 'viridis', 'plasma', 'rainbow', etc.
        plt.plot(time, trace, color=colors(int(replicate)), label=replicate)
        plt.title(f'Genotype : {genotype} {TREATMENT_NAME} :{light}')
        plt.show()