from pirk.calculations.pam import calculate_fluorescence_values
from pirk.parsing.helpers import add_object_column
from pirk.reporting.export import save_combined_df

from scripts.load_data import load_combined_df
from pirk.names import *

combined_df = load_combined_df(DEFAULT_DATA_PATH,FILE_NAME)

columns_to_add = [FS,FO_P,FM_P,PHI_2,NPQ_T,QL,PHI_NO,PHI_NPQ,QP,FV_FM_P]


for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=False)

indexes = combined_df[(combined_df[LABEL_COLUMN] == LABEL_PAM)].index

for index in [indexes[0]]:#indexes:
    calculate_fluorescence_values(combined_df, index,plot_all=True)

# save_combined_df(combined_df, FILE_NAME_PAM_FITS, DEFAULT_OUTPUT_PATH, file_format='pkl', overwrite=True)
