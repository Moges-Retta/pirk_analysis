import matplotlib.pyplot as plt

from pirk.names import ECS_Y_LABEL, LABEL_ECS, P700_Y_LABEL, MODEL_PREDICTION, LABEL_COLUMN, MODEL_TIME, TIME_CONSTANTS, \
    PIRK_AMPLITUDES, PIRK_TIMES, FLURO_Y_LABEL, LABEL_P700, TREATMENT_COLUMN, REPLICATE_COLUMN, GENOTYPE_COLUMN


def plot_trace_fits(combined_df, index,dirk_pirk_x,dirk_pirk_y,trace_x,trace_y,gH_values,relative_pirk_amplitudes,pirk_times):

    experiment_name = combined_df[LABEL_COLUMN][index]
    fig, ax1 = plt.subplots()
    fig.suptitle(f"index: {index}, experiment: {experiment_name}")
    ax1.plot(trace_x, dirk_pirk_y, 'g-', label=MODEL_PREDICTION)
    ax1.plot(trace_x, trace_y,'o', color='gray', alpha=0.5)

    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('Signal (a.u.)', color='g')
    ax1.tick_params(axis='y', labelcolor='g')

    ax2 = ax1.twinx()
    if experiment_name == LABEL_ECS:
        label = ECS_Y_LABEL
    elif experiment_name == LABEL_P700:
        label = P700_Y_LABEL
    else:
        label = FLURO_Y_LABEL

    # Plot gH_values versus dirk_pirk_x on the right y-axis
    ax2.plot(dirk_pirk_x, gH_values, 'b-', label=label)
    ax2.set_ylabel(label, color='b')
    ax2.tick_params(axis='y', labelcolor='b')

    # Create the third y-axis
    ax3 = ax1.twinx()

    # Offset the third y-axis
    ax3.spines['right'].set_position(('outward', 60))
    ax3.plot(pirk_times, relative_pirk_amplitudes, label=f'{PIRK_AMPLITUDES}', color='r', marker='o')
    ax3.set_ylabel('relative pirk amplitudes (a.u.)', color='r')
    ax3.tick_params(axis='y', labelcolor='r')
    ax1.set_ylim(ymin=-0.1)
    ax3.set_ylim(ymin=-0.1)

    plt.tight_layout()
    plt.show()

def plot_dirk_pirk_fit(combined_df, index, postprocessed, trace_x, trace_y):
    """
    Plot DIRK/PIRK trace fit results.

    Parameters
    ----------
    combined_df : pd.DataFrame
        DataFrame containing fitted results.
    index : int or str
        Row index in the DataFrame.
    postprocessed : dict
        Output from postprocess_dirk_pirk_fit().
    trace_x : np.ndarray
        Original x-values of the trace.
    trace_y : np.ndarray
        Original y-values of the trace.
    """
    plot_trace_fits(
        combined_df,
        index,
        postprocessed[MODEL_TIME],
        postprocessed[MODEL_PREDICTION],
        trace_x,
        trace_y,
        postprocessed[TIME_CONSTANTS],
        postprocessed[PIRK_AMPLITUDES],
        postprocessed[PIRK_TIMES]
    )

def plot_PAM(trace, light_intensity, genotype, replicate, figsize=(10, 3), color='red', save_path=None):
    """
    Plot a PAM signal trace.

    Parameters
    ----------
    trace : array-like
        PAM signal values.
    light_intensity : float
        Intensity increment used in the experiment.
    genotype : str
        Plant genotype.
    replicate : str or int
        Replicate identifier.
    figsize : tuple, optional
        Figure size. Default is (10, 3).
    color : str, optional
        Line color. Default is 'red'.
    save_path : str, optional
        If provided, saves the figure to this path instead of showing it.
    """
    plt.figure(figsize=figsize)
    plt.plot(trace, color=color, lw=1.5)
    plt.xlabel("Pulses (-)", fontsize=12)
    plt.ylabel("Fluorescence (590 nm)", fontsize=12)
    plt.title(f"PAM Signal | {GENOTYPE_COLUMN}: {genotype} | {REPLICATE_COLUMN}: {replicate} | {TREATMENT_COLUMN}={light_intensity}", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300)
        print(f"Figure saved to {save_path}")
        plt.close()
    else:
        plt.show()
