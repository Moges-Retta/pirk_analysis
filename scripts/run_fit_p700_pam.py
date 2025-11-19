from pirk import LABEL_PAM_P700
from pirk.calculations.p700_pam import calculate_ps1_all
from pirk.parsing.helpers import add_object_column
from pirk.reporting.export import save_combined_df

from scripts.load_data import load_combined_df

from pirk.names import *

combined_df = load_combined_df(DEFAULT_DATA_PATH,FILE_NAME)

# Protocol related inputs, from photorides 2.0
trace_indices = {
    PSI_SS_BEG:1,      # beginning of the trace for P700 steady-state
    PSI_SS_END:18,     # end of the trace for P700 steady-state
    PSI_SAT1_BEG:25,   # beginning of the trace for P700 first saturation pulse
    PSI_SAT1_END:170,  # end of the trace for P700 first saturation pulse
    PSI_DARK_BEG:195,  # beginning of the trace for P700 steady-state
    PSI_DARK_END:205,  # end of the trace for P700 steady-state
    PSI_SAT2_BEG:220,  # beginning of the trace for P700 second saturation pulse
    PSI_SAT2_END:270,  # end of the trace for P700 second saturation pulse
}

columns_to_add = [PSI_OX,PSI_ACT,PSI_OPEN,PSI_OR]

for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=False)

indexes = combined_df[(combined_df[LABEL_COLUMN] == LABEL_PAM_P700)].index

for index in indexes:
    calculate_ps1_all(combined_df,index,trace_indices,plot_all=False)

save_combined_df(combined_df, FILE_NAME_PAM_P700_FITS, DEFAULT_OUTPUT_PATH, file_format='pkl', overwrite=True)

