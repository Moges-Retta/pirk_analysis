import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_traces_genotype_replicate(
    trace, time, pirk_points, dirk_begin,
    genotype=None, replicate=None,
    trace_color='blue', pirk_color='yellow', pirk_size=8,
    shaded_color='lightgray', shaded_opacity=0.6
):
    """
    Plot a fluorescence trace with Pirk points and a shaded Dirk period.

    Parameters
    ----------
    trace : array-like
        Signal trace values.
    time : array-like
        Corresponding time values (ms or s).
    pirk_points : list or array of int
        Indices of Pirk points.
    dirk_begin : float
        Time value when Dirk period starts (shaded region).
    genotype : str, optional
        Genotype name to show in the title.
    replicate : int, optional
        Replicate number to show in the title.
    trace_color : str, optional
        Color of the trace line.
    pirk_color : str, optional
        Color of Pirk point markers.
    pirk_size : int, optional
        Marker size for Pirk points.
    shaded_color : str, optional
        Color of the shaded Dirk period.
    shaded_opacity : float, optional
        Opacity of the shaded Dirk period.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        Plotly figure object.
    """
    df = pd.DataFrame({'Time (ms)': time, 'Trace': trace})
    peak_trace = trace[pirk_points]
    peak_time = time[pirk_points]

    fig = px.scatter(df, x='Time (ms)', y='Trace', opacity=0)  # invisible scatter for layout

    # Add trace line
    fig.add_trace(go.Scatter(x=df['Time (ms)'], y=df['Trace'],
                             mode='lines', line=dict(color=trace_color),
                             name='Trace'))

    # Add Pirk points
    fig.add_trace(go.Scatter(x=peak_time, y=peak_trace,
                             mode='markers', name='Pirk points',
                             marker=dict(color=pirk_color, size=pirk_size)))

    # Add shaded Dirk period
    fig.add_vrect(x0=dirk_begin, x1=time[-1],
                  fillcolor=shaded_color, opacity=shaded_opacity,
                  layer="below", line_width=0, annotation_text="Dirk period", annotation_position="top left")

    # Update layout
    title_text = "Fluorescence Trace"
    if genotype is not None and replicate is not None:
        title_text += f" | Genotype: {genotype}, Replicate: {replicate}"

    fig.update_layout(
        template="plotly_white",
        title=dict(text=title_text, x=0.5, xanchor='center'),
        yaxis_title="Max normalized trace",
        xaxis_title="Time (ms)",
        font=dict(size=14)
    )

    fig.show()
    return fig
