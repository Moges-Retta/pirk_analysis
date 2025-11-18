# Fitting all the experimental data using the same initial guess could lead to unreliable fit
import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

from pirk.calculations.compute import find_steady_state_pirk_amplitudes
from pirk.fitting.models import construct_dirk_pirk, dirk_pirk
from pirk.parsing.cleaning import prep_traces_for_fitting
from pirk.parsing.loader import extract_Fluro_paras
from pirk.plotting.fits import plot_trace_fits


def fit_pirk_dirk(combined_df, index, guess_dict, plot_all=True):
    global pirk_points

    trace_x, trace_y, pirk_points, dirk_point_indexes = prep_traces_for_fitting(combined_df, index)

    # fixed parameters that define the protocol

    x_end = np.max(trace_x)
    x_total_points = len(trace_x)

    y_total = np.zeros(x_total_points)
    x_total = np.linspace(0, x_end, x_total_points)

    # parameters that could be fit to the data

    amplitude = guess_dict['amplitude']
    lifetime = guess_dict['lifetime']
    y_offset = guess_dict['y_offset']
    pirk_begin_amplitude = guess_dict['pirk_begin_amplitude']
    pirk_end_amplitude = guess_dict['pirk_end_amplitude']
    pirk_amplitude_recovery_lifetime = guess_dict['pirk_amplitude_recovery_lifetime']
    offset_amplitude = guess_dict['offset_amplitude']
    offset_lifetime = guess_dict['offset_lifetime']

    dirk_pirk_x, dirk_pirk_y, pirk_times, relative_pirk_amplitudes = construct_dirk_pirk(x_total, pirk_points,
                                                                                         amplitude,
                                                                                         lifetime, y_offset,
                                                                                         pirk_begin_amplitude,
                                                                                         pirk_end_amplitude,
                                                                                         pirk_amplitude_recovery_lifetime,
                                                                                         offset_amplitude,
                                                                                         offset_lifetime)

    # print("relative_pirk_amplitudes", relative_pirk_amplitudes)

    steady_state_pirk_x, steady_state_pirk_amplitude = find_steady_state_pirk_amplitudes(combined_df, index, dirk_par=0,
                                                                                         number_baseline_points=10)

    # print(steady_state_pirk_x, steady_state_pirk_amplitude)
    # print(x_total, trace_y)
    p0 = [amplitude,
          lifetime, y_offset,
          pirk_begin_amplitude, pirk_end_amplitude, pirk_amplitude_recovery_lifetime,
          offset_amplitude, offset_lifetime]

    bounds = ([0, 0, 0, 0, 0, 0, 0, 0],
              [np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    print("Fitting Analytical model...")
    import time

    t0 = time.time()
    fit_success = False
    rel_err = float('inf')  # Initialize with worst case
    max_attempts = 10
    threshold = 0.5
    attempt = 0

    # Try initial fit
    try:
        fit, pcov = curve_fit(dirk_pirk, x_total, trace_y, p0=p0, bounds=bounds, maxfev=100000, method='trf')
        perr = np.sqrt(np.diag(pcov))
        rel_err = abs(perr[0] / fit[0]) if fit[0] != 0 else float('inf')
        fit_success = True
    except RuntimeError as e:
        print(f"Initial fit failed: {e}")
        p0[0] = 0  # Reset parameter for retries

    # Retry loop if needed
    while (rel_err > threshold or np.round(rel_err, 3) == 0) and p0[0] < 5 and attempt < max_attempts:
        p0[0] += 100
        try:
            fit, pcov = curve_fit(dirk_pirk, x_total, trace_y, p0=p0, bounds=bounds, maxfev=100000, method='trf')
            perr = np.sqrt(np.diag(pcov))
            rel_err = abs(perr[0] / fit[0]) if fit[0] != 0 else float('inf')
            fit_success = True
        except RuntimeError as e:
            print(f"Retry {attempt + 1} failed: {e}")
            rel_err = float('inf')  # Force another attempt
        attempt += 1

    # Final report
    if not fit_success:
        # Populate with NaNs or defaults so the rest of the pipeline doesn't crash
        fit = [np.nan] * len(p0)
        pcov = np.full((len(p0), len(p0)), np.nan)
        perr = [np.nan] * len(p0)
        dirk_pirk_y = np.full_like(trace_y, np.nan)
        rmse = np.nan
        ci = [np.nan] * len(p0)
        print("⚠️ Curve fitting ultimately failed after retries.")
    else:
        print(f"✅ Fitting completed in {time.time() - t0:.2f} seconds.")

        dirk_pirk_x, dirk_pirk_y, pirk_times, relative_pirk_amplitudes = construct_dirk_pirk(x_total, pirk_points, *fit)

        pirk_times = [0] + pirk_times
        relative_pirk_amplitudes = [steady_state_pirk_amplitude] + relative_pirk_amplitudes

        plot_trace_fits(combined_df, index, dirk_pirk_x, dirk_pirk_y, trace_x, trace_y, gH_values,
                        relative_pirk_amplitudes, pirk_times)


        # Calculate standard errors
        perr = np.sqrt(np.diag(pcov))

        # Compute residuals (differences between actual and predicted)
        residuals = trace_y - dirk_pirk_y

        # Compute RMSE
        rmse = np.sqrt(np.mean(residuals ** 2))

        # Compute RMSE
        ci = 1.96 * np.sqrt(np.diag(pcov))

        labels = [
            'amplitude',
            'lifetime',
            'y_offset',
            'pirk_begin_amplitude',
            'pirk_end_amplitude',
            'pirk_amplitude_recovery_lifetime',
            'offset_amplitude',
            'offset_lifetime'
        ]

        # Print table
        threshold = 0.5  # Threshold: relative error > 0.5 considered unreliable

        print(
            f"\nFitted Parameters and Standard Errors index. {index} : genotype {combined_df['genotype'][index]} Replicate :{combined_df['replicate'][index]}\n")
        print(f"RMSE: {rmse:.3f}")

        print(f"{'Parameter':35} {'Value':>10} {'Std. Error':>12} {'95% CI':>15}")
        print("-" * 85)

        for label, val, err in zip(labels, fit, perr):
            rel_err = abs(err / val) if val != 0 else float('inf')
            ci_low = val - 1.96 * err
            ci_high = val + 1.96 * err

            if rel_err > threshold or np.round(err, 3) == 0:
                color_start = '\033[91m'  # Red for high relative error
                color_end = '\033[0m'
            else:
                color_start = ''
                color_end = ''

            print(f"{color_start}{label:35} {val:10.3f} {err:12.3f} [{ci_low:7.3f}, {ci_high:7.3f}]{color_end}")

        if plot_all:
            experiment_name = combined_df['trace_label'][index]
            fig, ax1 = plt.subplots()
            fig.suptitle(f"index: {index}, experiment: {experiment_name}")
            ax1.plot(dirk_pirk_x, dirk_pirk_y, 'g-', label='dirk_pirk_y')
            ax1.plot(trace_x, trace_y, color='gray', alpha=0.5)

            ax1.set_xlabel('time (s)')
            ax1.set_ylabel('Fluorescence signal (a.u.)', color='g')
            ax1.tick_params(axis='y', labelcolor='g')

            # Create the third y-axis
            ax3 = ax1.twinx()

            # Offset the third y-axis
            ax3.spines['right'].set_position(('outward', 60))
            ax3.plot(pirk_times, relative_pirk_amplitudes, label='pirk_amplitudes', color='r', marker='o')
            ax3.set_ylabel('relative pirk amplitudes (a.u.)', color='r')
            ax3.tick_params(axis='y', labelcolor='r')
            ax1.set_ylim(ymin=-0.1)
            ax3.set_ylim(ymin=-0.1)

            plt.tight_layout()
            plt.show()


def fit_fm_values(trace,indices,ramp_lights):

    f_values = extract_Fluro_paras(trace,indices)

    # SET THE INVERSE INTENSITIES FOR THE AVENSON INTENSITY RAMP
    inverse_intensity = [1 / r for r in ramp_lights]

    # Keys you want to extract
    selected_keys = ['AFmP', 'FmP_step2', 'FmP_step3','FmP_step4',"FmP_step5"]
    selected_values = [f_values[k] for k in selected_keys]

    # Calculations for corrected FmPrime using multi-phase flash
    slope, intercept = np.polyfit(inverse_intensity, selected_values, deg=1)

    return [slope,intercept]



