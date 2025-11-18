import os

import pandas as pd

from pirk.calculations.compute import calculate_ps1_all
from pirk.calculations.mpf import calculate_fvalues
from pirk.fitting.fitters import fit_pirk_dirk

from pirk.utils.helpers import add_object_column


filename = 'combined_df_processed_updated_corrected.pkl'
path = '/Users/retta001/Documents/Expt/Test_PRIK/'
full_path = os.path.join(path, filename)

combined_df = pd.read_pickle(full_path)


columns_to_add = [
    'dirk_pirk_fit_params',
    'pirk_times',
    'pirk_amplitudes',
    'steady_state_pirk_x',
    'steady_state_pirk_amplitude',
    'tau_values',
    'dirk_pirk_x',
    'dirk_pirk_y',
    'trace_x',
    'trace_y'
]

for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=False)

indexes = combined_df[(combined_df['trace_label'] == 'P700-pirk')].index
guess_dict = {
    'amplitude':0.5,
    'gH_start': 50,
    'gH_end': 100,
    'gH_lifetime': 0.08,
    'pirk_begin_amplitude': 0.5,
    'pirk_end_amplitude': 1,
    'pirk_amplitude_recovery_lifetime': 0.05,
    'offset_amplitude': 0.1,
    'offset_lifetime': 0.5
}

fit_pirk_dirk(combined_df, indexes[1], guess_dict, plot_all = True)


# Protocol related inputs, from photorides 2.0
trace_indices = {
    'PSI_ss_beg':1,      # beginning of the trace for P700 steady-state
    'PSI_ss_end':18,     # end of the trace for P700 steady-state
    'PSI_sat1_beg':25,   # beginning of the trace for P700 first saturation pulse
    'PSI_sat1_end':170,  # end of the trace for P700 first saturation pulse
    'PSI_dark_beg':195,  # beginning of the trace for P700 steady-state
    'PSI_dark_end':205,  # end of the trace for P700 steady-state
    'PSI_sat2_beg':220,  # beginning of the trace for P700 second saturation pulse
    'PSI_sat2_end':270,  # end of the trace for P700 second saturation pulse
}

columns_to_add = [
    'PSI_ox',
    'PSI_act',
    'PSI_open',
    'PSI_or'
]

for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=False)

indexes = combined_df[(combined_df['trace_label'] == 'PAM-P700')].index

for index in indexes:
    calculate_ps1_all(combined_df,index,trace_indices)



columns_to_add = [
    'Fs',
    'Fo_p',
    'Fm_p',
    'phi_2',
    'NPQ_t',
    'qL',
    'phi_NO',
    'phi_NPQ',
    'qP',
    'Fv_Fm_p'
]

for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=False)

indexes = combined_df[(combined_df['trace_label'] == 'PAM')].index

for index in indexes:
    calculate_fvalues(combined_df, index,plot_all=True)


