FILE_NAME = 'combined_df_processed.pkl'
FILE_NAME_PIRK_FITS = 'combined_df_PIRK_fits'
FILE_NAME_PAM_FITS = 'combined_df_PAM_fits'
FILE_NAME_PAM_P700_FITS = 'combined_df_PAM_P700_fits'

# -----------------------------
# Column names in combined_df
# -----------------------------
TIME_COLUMN = "trace_time"
TRACE_COLUMN = "trace"
PIRK_POINTS_COLUMN = "pirk_points"
DIRK_INDICES_COLUMN = "dirk_indices"
GENOTYPE_COLUMN = "genotype"
REPLICATE_COLUMN = "replicate"
LABEL_COLUMN = "trace_label"
TREATMENT_COLUMN = "light_intensity"
TREATMENT_NAME="Light",
LABEL_ECS = "ecs-pirk"
LABEL_P700 = "P700-pirk"
LABEL_FLURO = "fluro-pirk"
LABEL_PAM = "PAM"
LABEL_PAM_P700 = "PAM-P700"
NUMBER_PULSES="number_pulses"
# -----------------------------
# Column names in combined_df after fitting
# -----------------------------

FIT_PARAMS="dirk_pirk_fit_params"
PIRK_TIMES="pirk_times"
PIRK_AMPLITUDES= "pirk_amplitudes"
STEADY_STATE_PIRK_TIME="steady_state_pirk_x"
STEADY_STATE_PIRK_AMPLITUDE="steady_state_pirk_amplitude"
TIME_CONSTANTS="tau_values"
MODEL_TIME="dirk_pirk_x"
MODEL_PREDICTION="dirk_pirk_y"
TIME_FITTED="trace_x"
TRACE_FITTED="trace_y"

# -----------------------------
# Parameters for fitting
# -----------------------------

AMPLITUDE = "amplitude"
GH_START = "gH_start"
GH_END = "gH_end"
GH_LIFETIME = "gH_lifetime"
PIRK_BEGIN_AMPLITUDE = "pirk_begin_amplitude"
PIRK_END_AMPLITUDE = "pirk_end_amplitude"
PIRK_AMPLITUDE_RECOVERY_LIFETIME = "pirk_amplitude_recovery_lifetime"
OFFSET_AMPLITUDE = "offset_amplitude"
OFFSET_LIFETIME = "offset_lifetime"

# -----------------------------
# Fluorescence Parameters for fitting
# -----------------------------
AFMP = "AFmP"
FMP_STEP2 = "FmP_step2"
FMP_STEP3 = "FmP_step3"
FMP_STEP4 = "FmP_step4"
FMP_STEP5 = "FmP_step5"
RAMP_LIGHT= "RAMP_light"

# -----------------------------
# PAM P700 Fluorescence Parameters for fitting
# -----------------------------
FS = "Fs"
FO_P = "Fo_p"
FM_P = "Fm_p"
PHI_2 = "phi_2"
NPQ_T = "NPQ_t"
QL = "qL"
PHI_NO = "phi_NO"
PHI_NPQ = "phi_NPQ"
QP = "qP"
FV_FM_P = "Fv_Fm_p"

# -----------------------------
# PAM P700 Fluorescence fitting indices
# -----------------------------
PSI_SS_BEG = "PSI_ss_beg"
PSI_SS_END = "PSI_ss_end"
PSI_SAT1_BEG = "PSI_sat1_beg"
PSI_SAT1_END = "PSI_sat1_end"
PSI_DARK_BEG = "PSI_dark_beg"
PSI_DARK_END = "PSI_dark_end"
PSI_SAT2_BEG = "PSI_sat2_beg"
PSI_SAT2_END = "PSI_sat2_end"

PSI_OX = "PSI_ox"
PSI_ACT = "PSI_act"
PSI_OPEN = "PSI_open"
PSI_OR = "PSI_or"


# -----------------------------
# Standard file paths / directories (can be overridden)
# -----------------------------
DEFAULT_DATA_PATH = "/Users/retta001/Documents/Expt/pirk_analysis/pirk/data/"
DEFAULT_OUTPUT_PATH = "/Users/retta001/Documents/Expt/pirk_analysis/pirk/results/"

# -----------------------------
# Default parameters for baseline / fitting
# -----------------------------
BASELINE_BEGIN_TIME = 0.35  # seconds
BASELINE_END_TIME = 0.38    # seconds

FIG_SIZE_DEFAULT = (10, 3)

ECS_Y_LABEL = r'$g_{\mathrm{H}^+} \; (\mathrm{s}^{-1})$'
P700_Y_LABEL = r'$k_{{P700}} \; (\mathrm{s}^{-1})$'
FLURO_Y_LABEL = r'$\tau_{\mathrm{fluro}} \; (\mathrm{s}^{-1})$'

