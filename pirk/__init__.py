# pirk/__init__.py
from scripts import load_data
from scripts.load_data import load_combined_df
from .fitting.fitters import fit_pirk_dirk
from .fitting.model_basic import exp_decay, pirk_amplitude_recovery, exp_decay_with_variable_gH
from .fitting.models import construct_dirk_pirk, dirk_pirk
from .parsing.prep_data_fit import prep_traces_for_fitting
from .parsing.loader import parse_array, parse_indices
from .plotting.fits import plot_PAM
from .plotting.summaries import plot_all_dirk_pirk_fits
from .plotting.traces import plot_traces_genotype_replicate

from .names import *
from pirk.parsing.helpers import find_closest_index

# -----------------------------
# Package version
# -----------------------------
__version__ = "0.1.0"

# -----------------------------
# Expose public API
# -----------------------------

# Re-export selected names from names.py
from .names import (
    TIME_COLUMN,
    TRACE_COLUMN,
    PIRK_POINTS_COLUMN,
    DIRK_INDICES_COLUMN,
    GENOTYPE_COLUMN,
    REPLICATE_COLUMN,
    DEFAULT_DATA_PATH,
    DEFAULT_OUTPUT_PATH,
    BASELINE_BEGIN_TIME,
    BASELINE_END_TIME,
    FIG_SIZE_DEFAULT,
    FILE_NAME_PIRK_FITS
)

__all__ = [
    "prep_traces_for_fitting",
    "parse_array",
    "parse_indices",
    "fit_pirk_dirk",
    "construct_dirk_pirk",
    "dirk_pirk",
    "exp_decay",
    "exp_decay_with_variable_gH",
    "pirk_amplitude_recovery",
    "find_closest_index",
    "plot_PAM",
    "plot_traces_genotype_replicate",
    "print_fit_table",
    "load_combined_df",
    "save_combined_df",
    "load_data",
    "plot_all_dirk_pirk_fits",
    "TIME_COLUMN",
    "TRACE_COLUMN",
    "PIRK_POINTS_COLUMN",
    "DIRK_INDICES_COLUMN",
    "GENOTYPE_COLUMN",
    "REPLICATE_COLUMN",
    "DEFAULT_DATA_PATH",
    "DEFAULT_OUTPUT_PATH",
    "BASELINE_BEGIN_TIME",
    "BASELINE_END_TIME",
    "FIG_SIZE_DEFAULT",
    "FIT_PARAMS",
    "PIRK_TIMES",
    "PIRK_AMPLITUDES",
    "STEADY_STATE_PIRK_TIME",
    "STEADY_STATE_PIRK_AMPLITUDE",
    "TIME_CONSTANTS",
    "MODEL_TIME",
    "MODEL_PREDICTION",
    "TIME_FITTED",
    "TRACE_FITTED",
    "ECS_Y_LABEL",
    "P700_Y_LABEL",
    "TREATMENT_COLUMN",
    "TREATMENT_NAME",
    "LABEL_ECS",
    "LABEL_P700",
    "LABEL_FLURO",
    "LABEL_PAM",
    "LABEL_PAM_P700"
]

from .reporting.export import save_combined_df

from .reporting.tables import print_fit_table

