import os
from functools import wraps

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px


def save_fig(file_path="plot.html", auto_open=False):
    """
    Decorator to save a Plotly figure to a file.

    Parameters:
    file_path (str): The path where the plot will be saved.
    auto_open (bool): Automatically open the plot file after saving.

    Returns:
    Decorated function.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Execute the plotting function
            fig = func(*args, **kwargs)

            # Save the figure
            if file_path.endswith(".html"):
                fig.write_html(file_path, auto_open=auto_open)
            elif file_path.endswith(".png"):
                fig.write_image(file_path)
            else:
                raise ValueError("Unsupported file format: Please use .html or .png")

            return fig

        return wrapper

    return decorator


@save_fig(file_path="boxplot.html", auto_open=True)
def boxplot_plotly(df, cols, title, color_points=False):
    """
    Generates interactive boxplots with point identification for one or multiple columns in a DataFrame using Plotly.

    Parameters:
    df (pd.DataFrame): DataFrame containing data to be plotted.
    cols (str or list of str): Name(s) of the DataFrame column(s) to plot. Can be a single string or a list of strings.
    title (str): Title of the plot.
    color_points (bool): If True, each point is colored individually. If False, all points are the same color.

    Returns:
    None: The function only displays the plot.
    """
    # Ensure cols is a list
    if isinstance(cols, str):
        cols = [lan(cols)]

    num_cols = len(cols)
    num_rows = (num_cols + 1) // 2  # Calculate rows needed for up to 2 plots per row

    fig = make_subplots(rows=num_rows, cols=2, subplot_titles=cols)

    # Define a unique color palette for points if color_points is True
    colors = px.colors.qualitative.Plotly if color_points else ["blue"]

    for i, col in enumerate(cols):
        row = (i // 2) + 1
        col_idx = (i % 2) + 1

        fig.add_trace(
            go.Box(
                y=df[col],
                name=col,
                boxpoints="all",  # Display all points
                jitter=0.5,  # Spread points to reduce overlap
                pointpos=0,  # Position points relative to box
                marker=dict(color="lightblue"),
                line=dict(color="darkblue"),
            ),
            row=row,
            col=col_idx,
        )

        # Optionally add individual point colors
        if color_points:
            for idx, value in enumerate(df[col]):
                fig.add_trace(
                    go.Scatter(
                        x=[
                            col for _ in df[col]
                        ],  # Necessary to align points with boxplot
                        y=[value],
                        mode="markers",
                        marker=dict(color=colors[idx % len(colors)], size=8),
                        showlegend=False,
                    ),
                    row=row,
                    col=col_idx,
                )

    fig.update_layout(
        title_text=title,
        height=400 * num_rows,  # Adjust height based on the number of rows
        showlegend=False,
    )

    return fig
