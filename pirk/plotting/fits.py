import matplotlib.pyplot as plt

def plot_trace_fits(combined_df, index,dirk_pirk_x,dirk_pirk_y,trace_x,trace_y,gH_values,relative_pirk_amplitudes,pirk_times):
    experiment_name = combined_df['trace_label'][index]
    fig, ax1 = plt.subplots()
    fig.suptitle(f"index: {index}, experiment: {experiment_name}")
    ax1.plot(dirk_pirk_x, dirk_pirk_y, 'g-', label='dirk_pirk_y')
    ax1.plot(trace_x, trace_y, color='gray', alpha=0.5)

    ax1.set_xlabel('time (s)')
    ax1.set_ylabel('ECS signal (a.u.)', color='g')
    ax1.tick_params(axis='y', labelcolor='g')

    ax2 = ax1.twinx()

    # Plot gH_values versus dirk_pirk_x on the right y-axis
    ax2.plot(dirk_pirk_x, gH_values, 'b-', label='k_P700')
    ax2.set_ylabel(r'$k_{P700} \; (s^{-1})$', color='b')
    ax2.tick_params(axis='y', labelcolor='b')

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