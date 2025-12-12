import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from pirk.fitting.fitters import prep_traces_for_fitting
from pirk.names import *

from pirk.parsing.helpers import add_object_column

def plot_corr_matrix(pcov, labels):
    lower_triangle = np.tril(pcov)

    param_std = np.sqrt(np.diag(pcov))  # Standard deviations
    outer_std = np.outer(param_std, param_std)

    # Avoid division by zero
    with np.errstate(divide='ignore', invalid='ignore'):
        corr_matrix = np.divide(pcov, outer_std)
        corr_matrix[~np.isfinite(corr_matrix)] = 0  # Replace nan/inf with 0

        # Create mask for upper triangle
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

    # Plot only lower triangle
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, xticklabels=labels, yticklabels=labels,
                mask=mask, annot=True, fmt=".2f", cmap='coolwarm', vmin=-1, vmax=1)
    plt.title("Lower Triangle of Correlation Matrix")
    plt.tight_layout()
    plt.show()


def plot_MPF_noMPF(fluro_values):

    width = 0.35
    i_incs = list(fluro_values.keys())
    index = range(len(i_incs))

    metrics = {
            "fvfm": r"$\phi_{II}$",
            "qL": "qL",
            "npqt": "NPQt",
            "PhiNPQ": r"$\phi_{NPQ}$",
            "PhiNO": r"$\phi_{NO}$"
        }

    for base_key, label in metrics.items():
        mpf_vals = [fluro_values[i][f"{base_key}_MPF"] for i in i_incs]
        no_mpf_vals = [fluro_values[i][f"{base_key}_noMPF"] for i in i_incs]

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.bar(index, mpf_vals, width, label='MPF')
        ax.bar([i + width for i in index], no_mpf_vals, width, label='noMPF')
        ax.set_xticks([i + width / 2 for i in index])
        ax.set_xticklabels(i_incs)
        ax.set_xlabel("Light Intensity")
        ax.set_ylabel(label)
        ax.set_title(f"{label} Comparison (MPF vs. no MPF)")
        ax.legend()


# Function to set the global limits for all axes in a list of figures
def set_global_limits(figures):
    i = 0
    for ax in figures[i].get_axes():
        x_min, x_max = float('inf'), float('-inf')
        y_min, y_max = float('inf'), float('-inf')
    for i in range(0, len(figures)):

        for fig in figures:
            x_min_ax, x_max_ax = ax.get_xlim()
            y_min_ax, y_max_ax = ax.get_ylim()
            x_min = min(x_min, x_min_ax)
            x_max = max(x_max, x_max_ax)
            y_min = min(y_min, y_min_ax)
            y_max = max(y_max, y_max_ax)

        # for fig in figures:
        #     for ax in fig.get_axes():
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)


def _plot_dirk_pirk_fits(combined_df, index, ax1, ax2, ax3):
    trace_x, trace_y, pirk_points, dirk_point_indexes = prep_traces_for_fitting(combined_df, index)

    dirk_pirk_x = combined_df[MODEL_TIME][index]
    dirk_pirk_y = combined_df[MODEL_PREDICTION][index]
    ax1.plot(dirk_pirk_x, dirk_pirk_y, 'g-', label=MODEL_TIME)

    ax1.plot(trace_x, trace_y, color='gray', alpha=0.5)

    # Plot gH_values versus dirk_pirk_x on the right y-axis

    gH_values = combined_df[TIME_CONSTANTS][index]

    ax2.plot(dirk_pirk_x, gH_values, 'b-', label=TIME_CONSTANTS)

    # Offset the third y-axis
    ax3.spines['right'].set_position(('outward', 60))
    pirk_times = combined_df[PIRK_TIMES][index]
    relative_pirk_amplitudes = combined_df[PIRK_AMPLITUDES][index]
    relative_pirk_amplitudes[0]=combined_df[FIT_PARAMS][index][0] # FIXME!!!

    if len(pirk_times) > 0 and len(relative_pirk_amplitudes) > 0:
        ax3.plot(pirk_times, relative_pirk_amplitudes, label=PIRK_AMPLITUDES, color='r', marker='o')


def plot_all_dirk_pirk_fits(combined_df,trace_label):
    # List of genotypes to plot
    genotypes = combined_df[GENOTYPE_COLUMN].unique()

    # Unique light intensities across the dataset
    light_intensities = combined_df[TREATMENT_COLUMN].unique()

    figures = []

    # Loop over each genotype and light intensity
    for genotype in genotypes:
        for li in light_intensities:

            fig, ax1 = plt.subplots()

            ax1.set_xlabel('time (s)')
            ax1.set_ylabel('Signal (a.u.)', color='g')
            ax1.tick_params(axis='y', labelcolor='g')

            ax2 = ax1.twinx()

            if trace_label == LABEL_ECS:
                label = ECS_Y_LABEL
            elif trace_label == LABEL_P700:
                label = P700_Y_LABEL
            else:
                label = FLURO_Y_LABEL

            ax2.set_ylabel(label, color='b')
            ax2.tick_params(axis='y', labelcolor='b')

            ax3 = ax1.twinx()
            ax3.set_frame_on(True)
            ax3.spines['right'].set_position(('outward', 60))
            ax3.set_ylabel('Relative pirk amplitudes (a.u.)', color='r')
            ax3.tick_params(axis='y', labelcolor='r')
            plt.suptitle(f"{genotype}, {TREATMENT_NAME}: {li}")

            # Filter by genotype AND light intensity
            indexes = combined_df[
                (combined_df[LABEL_COLUMN] == trace_label) &
                (combined_df[GENOTYPE_COLUMN] == genotype) &
                (combined_df[TREATMENT_COLUMN] == li)
                ].index

            for index in indexes:
                _plot_dirk_pirk_fits(combined_df, index, ax1, ax2, ax3)

            plt.tight_layout()

            figures.append(fig)

        set_global_limits(figures)
        plt.show()



def extract_scaler_values_from_array(combined_df, col_name, from_col_name, protocol_label, value_index):
    """Extract a scalar from an array in a DataFrame column and store it in a new column."""
    add_object_column(combined_df, col_name)
    indexes = combined_df[combined_df[LABEL_COLUMN] == protocol_label].index
    for index in indexes:
        arr = combined_df[from_col_name][index]
        if arr is not None and len(arr) > 0:
            try:
                combined_df.at[index, col_name] = arr[value_index]
            except IndexError:
                combined_df.at[index, col_name] = np.nan  # fallback if index is too large
        else:
            combined_df.at[index, col_name] = np.nan  # empty array → store NaN
    return combined_df


def plot_extracted_params(combined_df,trace_labels):
    # === Define all parameters to extract ===
    extracted_parameters = {
        'steady state gH+': [TIME_CONSTANTS, trace_labels, 0],
        'relaxed gH+': [TIME_CONSTANTS, trace_labels, -1],
        'steady state pirk': [PIRK_AMPLITUDES, trace_labels, 0],
        'relaxed pirk': [PIRK_AMPLITUDES, trace_labels, -1],
        'ECSt': ['dirk_pirk_y', trace_labels, 0],
        'signal_amplitude': [FIT_PARAMS, trace_labels, 0],
        'gH_start': [FIT_PARAMS, trace_labels, 1],
        'gH_end': [FIT_PARAMS, trace_labels, 2],
        'gH_lifetime': [FIT_PARAMS, trace_labels, 3],
        'pirk_begin_amplitude': [FIT_PARAMS, trace_labels, 4],
        'pirk_end_amplitude': [FIT_PARAMS, trace_labels, 5],
        'pirk_amplitude_recovery_lifetime': [FIT_PARAMS, trace_labels, 6],
        'slow_phase_amplitude': [FIT_PARAMS, trace_labels, 7],
        'slow_phase_lifetime': [FIT_PARAMS, trace_labels, 8],
    }

    genotypes = combined_df[GENOTYPE_COLUMN].unique()

    parameter_plots = {}

    # === Extract all parameters ===
    for param, (from_col_name, protocol_label, value_index) in extracted_parameters.items():
        extract_scaler_values_from_array(combined_df, param, from_col_name, protocol_label, value_index)
        parameter_plots[param] = [param,GENOTYPE_COLUMN, protocol_label]

    # === Add derived parameter ===
    add_object_column(combined_df, 'total_fit_amplitude')
    indexes = combined_df[combined_df['trace_label'] == trace_labels].index
    for index in indexes:
        combined_df.at[index, 'total_fit_amplitude'] = (
            np.array(combined_df['signal_amplitude'][index]) +
            np.array(combined_df['slow_phase_amplitude'][index])
        )

    parameter_plots['total_fit_amplitude'] = ['total_fit_amplitude', 'genotype', trace_labels]

    # === Plot parameters ===
    unique_treatments = combined_df[TREATMENT_COLUMN].unique()

    # use matplotlib's default color cycle
    default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # extend colors automatically if needed
    while len(default_colors) < len(unique_treatments):
        default_colors = default_colors + default_colors

    colors = {t: c for t, c in zip(unique_treatments, default_colors)}

    for parameter, (col_name, x_col, protocol_label) in parameter_plots.items():
        fig, ax = plt.subplots(figsize=(15, 8))

        # loop over light intensities and genotypes
        for li in combined_df[TREATMENT_COLUMN].unique():
            for genotype in genotypes:  # your 52 genotypes
                indexes = combined_df[
                    (combined_df[LABEL_COLUMN] == protocol_label) &
                    (combined_df[GENOTYPE_COLUMN] == genotype) &
                    (combined_df[TREATMENT_COLUMN] == li)
                ].index

                if len(indexes) > 0:
                    x = np.array(combined_df[x_col][indexes])
                    y = np.array(combined_df[col_name][indexes])
                    ax.plot(x, y, marker='o', color=colors[li], alpha=0.7)

        # labels and title
        ax.set_xlabel(x_col)
        ax.set_ylabel(parameter)
        ax.set_title(parameter)

        # rotate x-axis labels
        plt.setp(ax.get_xticklabels(), rotation=90)

        # show legend only for light intensities
        handles = [plt.Line2D([0], [0], color=c, marker='o', linestyle='-', label=f"{TREATMENT_NAME} {li}")
                   for li, c in colors.items()]
        ax.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, -0.25), ncol=2)

        plt.tight_layout()
        plt.show()


