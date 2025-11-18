import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt


def plot_traces_genotype_replicate(trace, time, pirk_points, dirk_begin):
    df = pd.DataFrame({
        'Time (ms)': time,
        'Trace': trace})

    peak_trace = trace[pirk_points]
    peak_time = time[pirk_points]

    fig = px.scatter(df, x='Time (ms)', y='Trace')
    fig.add_trace(go.Scatter(x=df['Time (ms)'], y=df['Trace'], mode='lines'))
    fig.add_trace(
        go.Scatter(x=peak_time, y=peak_trace, mode='markers', name='Pirk points', marker=dict(color='yellow', size=8)))

    # Add shaded region from t_off to end
    fig.add_vrect(x0=dirk_begin, x1=time[-1],
                  fillcolor="lightgray", opacity=0.6,
                  layer="below", line_width=0)

    fig.update_layout(
        template="plotly_white",
        yaxis_title=dict(text="max normalized trace ", font=dict(size=18)),  # Custom x-axis label font size
    )
    fig.show()


def plot_PAM(trace, i_inc, genotype, replicate, color='red', figsize=(10, 3)):
    """
    Plot a PAM (Pulse-Amplitude Modulation) signal.

    Parameters
    ----------
    trace : array-like
        Signal values to plot.
    i_inc : float or int
        Light intensity increment.
    genotype : str
        Plant genotype.
    replicate : int
        Replicate number.
    color : str, optional
        Line color (default 'red').
    figsize : tuple, optional
        Figure size (default (10, 3)).

    Returns
    -------
    fig, ax : matplotlib.figure.Figure, matplotlib.axes.Axes
        Figure and axes objects for further customization.
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(trace, color=color, linewidth=1.5)
    ax.set_xlabel("Pulse number")
    ax.set_ylabel("Fluorescence (a.u.)")  # Replace with correct units if known
    ax.set_title(f"PAM Signal | Genotype: {genotype}, Replicate: {replicate}, Iinc={i_inc}")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

    return fig, ax
