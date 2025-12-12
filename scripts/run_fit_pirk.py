from pirk.calculations.pirk import find_steady_state_pirk_amplitudes
from pirk.fitting.fitters import fit_pirk_dirk
from pirk.plotting.fits import plot_dirk_pirk_fit
from pirk.reporting.export import save_combined_df

from pirk.parsing.helpers import add_object_column
from pirk.reporting.printing import report_dirk_pirk_fit
from scripts.load_data import load_combined_df
from pirk.names import *

combined_df = load_combined_df(DEFAULT_DATA_PATH,FILE_NAME)


columns_to_add = [
    FIT_PARAMS,
    PIRK_TIMES,
    PIRK_AMPLITUDES,
    STEADY_STATE_PIRK_TIME,
    STEADY_STATE_PIRK_AMPLITUDE,
    TIME_CONSTANTS,
    MODEL_TIME,
    MODEL_PREDICTION,
    TIME_FITTED,
    TRACE_FITTED
    ]


for col in columns_to_add:
    combined_df = add_object_column(combined_df, col, default_content=[], replace=True)

guess_dict = {
    AMPLITUDE:0.3,
    GH_START: 10,
    GH_END: 110,
    GH_LIFETIME: 0.08,
    PIRK_BEGIN_AMPLITUDE: 0.05,
    PIRK_END_AMPLITUDE: 2,
    PIRK_AMPLITUDE_RECOVERY_LIFETIME: 0.05,
    OFFSET_AMPLITUDE: 0.25,
    OFFSET_LIFETIME: 0.05
}
#
trace_to_fit_list = [LABEL_ECS]#,LABEL_P700,LABEL_FLURO]

indexes = combined_df[
    (combined_df[LABEL_COLUMN].isin(trace_to_fit_list))&
    (combined_df[GENOTYPE_COLUMN]=='Col-0')
    ].index
index = indexes[1]


fit, pcov, perr, postprocessed = fit_pirk_dirk(combined_df, index, guess_dict)

# Optional reporting
report_dirk_pirk_fit(combined_df, index, guess_dict, fit, pcov,
                     trace_y=combined_df.at[index, TRACE_FITTED],
                     dirk_pirk_y=postprocessed[MODEL_PREDICTION])
#
# Optional plotting
plot_dirk_pirk_fit(combined_df, index, postprocessed,
                   trace_x=combined_df.at[index, TIME_FITTED],
                   trace_y=combined_df.at[index,TRACE_FITTED])


# trace_to_fit_list = [LABEL_ECS,LABEL_P700,LABEL_FLURO]
#
# indexes = combined_df[combined_df[LABEL_COLUMN].isin(trace_to_fit_list)].index
# #
# for index in indexes:
#     fit, pcov, perr, postprocessed = fit_pirk_dirk(combined_df, index, guess_dict)
#
#     # Optional reporting
#     report_dirk_pirk_fit(combined_df, index, guess_dict, fit, pcov,
#                          trace_y=combined_df.at[index, TRACE_FITTED],
#                          dirk_pirk_y=postprocessed[MODEL_PREDICTION])
#
#     # # Optional plotting
#     # plot_dirk_pirk_fit(combined_df, index, postprocessed,
#     #                    trace_x=combined_df.at[index, TIME_FITTED],
#     #                    trace_y=combined_df.at[index, TRACE_FITTED])
#
# save_combined_df(combined_df, FILE_NAME_PIRK_FITS, DEFAULT_OUTPUT_PATH, file_format='pkl', overwrite=True)