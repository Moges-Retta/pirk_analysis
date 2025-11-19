from pirk.names import DEFAULT_OUTPUT_PATH, FILE_NAME, FILE_NAME_PIRK_FITS, LABEL_ECS,LABEL_P700
from pirk.plotting.summaries import plot_extracted_params, plot_all_dirk_pirk_fits
from pirk.reporting.export import save_combined_df
from scripts.load_data import load_combined_df

combined_df = load_combined_df(DEFAULT_OUTPUT_PATH,FILE_NAME_PIRK_FITS)

plot_all_dirk_pirk_fits(combined_df,LABEL_ECS)

plot_extracted_params(combined_df,LABEL_ECS)
# save_combined_df(combined_df, FILE_NAME_PIRK_FITS, DEFAULT_OUTPUT_PATH, file_format='pkl', overwrite=True)
#
# plot_all_dirk_pirk_fits(combined_df,LABEL_P700)
# plot_extracted_params(combined_df,LABEL_P700)
# save_combined_df(combined_df, FILE_NAME_PIRK_FITS, DEFAULT_OUTPUT_PATH, file_format='pkl', overwrite=True)
#
