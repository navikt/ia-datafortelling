from IPython.core.display import Markdown
from plotly import graph_objects as go
from plotly.graph_objs import Figure
import pandas as pd
from tabulate import tabulate


def create_bar_plot_with_button(
    list_of_series: list, labels: list, default_active=0, xrangeslider=0, **kwargs
) -> Figure:
    fig = go.Figure()

    for i, series in enumerate(list_of_series):
        fig.add_trace(
            go.Bar(
                visible=(i == default_active),
                x=series.index,
                y=series.values,
                name=labels[i],
            )
        )

    # Add button
    fig.update_layout(
        width=1100,
        height=600,
        updatemenus=[
            dict(
                active=default_active,
                type="buttons",
                direction="left",
                buttons=[
                    # One dict for each button, indicating which trace/graf to show
                    # Parameter visible is True for the respective button, and False for the remaining
                    # Example with three buttons:
                    # [True, False, False], [False, True, False], [False, False, True]
                    dict(
                        args=[
                            {
                                "visible": [
                                    button_i == button
                                    for button_i, label_i in enumerate(labels)
                                ]
                            }
                        ],
                        label=label,
                        method="update",
                    )
                    for button, label in enumerate(labels)
                ],
                showactive=True,
                xanchor="left",
                yanchor="top",
                x=0,
                y=1.1,
            ),
        ],
        **kwargs,
    )

    # Create slider
    if xrangeslider:
        fig.update_layout(
            height=700,
            xaxis=dict(autorange=True, rangeslider=dict(autorange=True, visible=True)),
        )

    return fig


def create_bar_plot(
    series: pd.Series,
    label: str,
) -> Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            visible=True,
            x=series.index,
            y=series.values,
        )
    )

    return fig


def create_cumulative_histogram(data_frame, x_col, label_col, xaxis, **kwargs):
    fig = go.Figure()

    for label in data_frame[label_col].unique():
        fig.add_trace(
            go.Histogram(
                x=data_frame.loc[data_frame[label_col] == label, x_col],
                name=str(label),
                cumulative_enabled=True,
                opacity=0.5,
            )
        )

    fig.update_xaxes(type="category", categoryarray=xaxis)

    fig.update_layout(
        width=1100,
        height=800,
        barmode="overlay",
        bargap=0,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        **kwargs,
    )

    return fig


def create_table(data) -> Markdown:
    # table = pd.pivot_table(data)
    return Markdown(tabulate(data.to_numpy(), headers=data.columns))


def formater_tittel(overskrift, undertekst):
    return f"<br><span style='font-size:1em;color:gray'>{overskrift}<br><span style='font-size:0.7em;color:gray'>{undertekst}"
