# Fitting all the experimental data using the same initial guess could lead to unreliable fit
import numpy as np
from scipy.optimize import curve_fit
from pirk.names import *

from pirk.calculations.pirk import find_steady_state_pirk_amplitudes
from pirk.fitting.models import construct_dirk_pirk, dirk_pirk
from pirk.parsing.prep_data_fit import prep_traces_for_fitting
from pirk.parsing.loader import extract_Fluro_paras
from pirk.plotting.fits import plot_trace_fits
from pirk.reporting.printing import print_fit_table

def run_dirk_pirk_fit(x_total, trace_y, p0, pirk_points, max_attempts=10, threshold=0.5):
    """
    Run curve_fit with retry logic.
    Returns: fit, pcov, perr, fit_success
    """
    n = len(p0)
    bounds = ([0] * n, [np.inf] * n)

    fit_success = False
    rel_err = float('inf')
    attempt = 0

    weights = np.ones_like(trace_y)
    peak_indices = np.where(trace_y > np.percentile(trace_y, 95))[0]  # top 5% as peaks
    weights[peak_indices] = 1  # smaller sigma → higher weight

    try:
        fit, pcov = curve_fit(
            lambda x, *params: dirk_pirk(x, *params, pirk_points),
            x_total,
            trace_y,
            p0=p0,
            bounds=bounds,
            sigma = weights,
            maxfev=100_000,
            method='trf'
        )
        perr = np.sqrt(np.diag(pcov))
        rel_err = abs(perr[0] / fit[0]) if fit[0] != 0 else float('inf')
        fit_success = True
    except RuntimeError as e:
        print(f"Initial fit failed: {e}")
        p0[0] = 0  # Reset first parameter for retries

    # Retry loop
    while (rel_err > threshold or np.round(rel_err, 3) == 0) and p0[0] < 5 and attempt < max_attempts:
        p0[0] += 100
        try:
            fit, pcov = curve_fit(
                lambda x, *params: dirk_pirk(x, *params, pirk_points),
                x_total,
                trace_y,
                p0=p0,
                bounds=bounds,
                sigma = weights,
                maxfev=100_000,
                method='trf'
            )
            perr = np.sqrt(np.diag(pcov))
            rel_err = abs(perr[0] / fit[0]) if fit[0] != 0 else float('inf')
            fit_success = True
        except RuntimeError as e:
            print(f"Retry {attempt + 1} failed: {e}")
            rel_err = float('inf')
        attempt += 1

    return fit, pcov, perr, fit_success

def postprocess_dirk_pirk_fit(fit, pirk_points, x_total, trace_y, combined_df, index):
    """
    Compute model outputs, time constants, relative amplitudes.
    """
    dirk_pirk_x, dirk_pirk_y, gH_values, pirk_times, relative_pirk_amplitudes = construct_dirk_pirk(
        x_total, pirk_points, *fit
    )

    steady_state_pirk_x, steady_state_pirk_amplitude = find_steady_state_pirk_amplitudes(
        combined_df, index, dirk_par=0, number_baseline_points=10
    )
    pirk_times = [0] + pirk_times

    steady_state_pirk_amplitude = steady_state_pirk_amplitude*1000 if combined_df.at[index,LABEL_COLUMN] in [LABEL_ECS,LABEL_P700] else steady_state_pirk_amplitude

    relative_pirk_amplitudes = [steady_state_pirk_amplitude] + relative_pirk_amplitudes

    return {
        MODEL_TIME: dirk_pirk_x,
        MODEL_PREDICTION: dirk_pirk_y,
        TIME_CONSTANTS: gH_values,
        PIRK_TIMES: pirk_times,
        PIRK_AMPLITUDES: relative_pirk_amplitudes,
        STEADY_STATE_PIRK_TIME: steady_state_pirk_x,
        STEADY_STATE_PIRK_AMPLITUDE: steady_state_pirk_amplitude
    }


def update_combined_df_with_fit(combined_df, index, fit, postprocessed, trace_x, trace_y):
    combined_df.at[index, FIT_PARAMS] = fit
    combined_df.at[index, STEADY_STATE_PIRK_TIME] = postprocessed[STEADY_STATE_PIRK_TIME]
    combined_df.at[index, STEADY_STATE_PIRK_AMPLITUDE] = postprocessed[STEADY_STATE_PIRK_AMPLITUDE]
    combined_df.at[index, TIME_CONSTANTS] = postprocessed[TIME_CONSTANTS]
    combined_df.at[index, MODEL_TIME] = postprocessed[MODEL_TIME]
    combined_df.at[index, MODEL_PREDICTION] = postprocessed[MODEL_PREDICTION]
    combined_df.at[index, PIRK_AMPLITUDES] = postprocessed[PIRK_AMPLITUDES]
    combined_df.at[index, PIRK_TIMES] = postprocessed[PIRK_TIMES]
    combined_df.at[index, TIME_FITTED] = trace_x
    combined_df.at[index, TRACE_FITTED] = trace_y


def fit_pirk_dirk(combined_df, index, guess_dict):
    """
    Compute DIRK/PIRK fit and update DataFrame.
    No plotting or printing.
    """
    trace_x, trace_y, pirk_points, dirk_point_indexes = prep_traces_for_fitting(combined_df, index)
    x_end = np.max(trace_x)
    x_total_points = len(trace_x)
    x_total = np.linspace(0, x_end, x_total_points)

    p0 = [
        guess_dict[AMPLITUDE],
        guess_dict[GH_START],
        guess_dict[GH_END],
        guess_dict[GH_LIFETIME],
        guess_dict[PIRK_BEGIN_AMPLITUDE],
        guess_dict[PIRK_END_AMPLITUDE],
        guess_dict[PIRK_AMPLITUDE_RECOVERY_LIFETIME],
        guess_dict[OFFSET_AMPLITUDE],
        guess_dict[OFFSET_LIFETIME]
    ]


    fit, pcov, perr, fit_success = run_dirk_pirk_fit(x_total, trace_y, p0, pirk_points)

    if not fit_success:
        fit = [np.nan] * len(p0)
        pcov = np.full((len(p0), len(p0)), np.nan)
        perr = [np.nan] * len(p0)
        postprocessed = {
            "dirk_pirk_x": np.full_like(trace_x, np.nan),
            "dirk_pirk_y": np.full_like(trace_y, np.nan),
            "gH_values": [np.nan] * len(p0),
            "pirk_times": [np.nan] * len(p0),
            "relative_pirk_amplitudes": [np.nan] * len(p0),
            "steady_state_pirk_x": np.nan,
            "steady_state_pirk_amplitude": np.nan
        }
    else:
        postprocessed = postprocess_dirk_pirk_fit(fit, pirk_points, x_total, trace_y, combined_df, index)

    update_combined_df_with_fit(combined_df, index, fit, postprocessed, trace_x, trace_y)

    return fit, pcov, perr, postprocessed


def fit_fm_values(trace,indices,ramp_lights):

    f_values = extract_Fluro_paras(trace,indices)

    # SET THE INVERSE INTENSITIES FOR THE AVENSON INTENSITY RAMP
    inverse_intensity = [1 / r for r in ramp_lights]

    # Keys you want to extract
    selected_keys = [AFMP, FMP_STEP2, FMP_STEP3,FMP_STEP4,FMP_STEP5]
    selected_values = [f_values[k] for k in selected_keys]

    # Calculations for corrected FmPrime using multiphase flash
    slope, intercept = np.polyfit(inverse_intensity, selected_values, deg=1)

    return [slope,intercept]



