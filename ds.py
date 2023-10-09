import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as plio
from IPython.core.display import Markdown, display_markdown
from datastory.datastory import DataStory
from plotly.graph_objs import Figure
from tabulate import tabulate


def create_bar_plot(data, **kwargs) -> str:
    fig = px.bar(data, width=1100, height=600, **kwargs)
    return plio.to_json(fig)


def create_line_plot(data, **kwargs):
    fig = px.line(data, width=1100, **kwargs)
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
    return fig


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


def create_datastory(preppede_data: {}) -> DataStory:
    ds = DataStory(name="Leverte IA-tjenester")
    ds.header(content="Leverte digitale IA-tjenester")
    ds.markdown(
        f""" 
    Statistikken på denne siden viser antall digitale IA-tjenester. 
    Dataregistreringen startet mars 2021.
    
    En digital IA-tjeneste telles når en bruker har benyttet seg av innholdet i 
    tjenesten. Det er ikke tilstrekkelig at brukeren kun har besøkt forsiden.
    """
    )
    ds.header(content="Unike virksomheter")
    for år, verdi in preppede_data["unike_bedrifter_per_år"].items():
        ds.markdown(f"- {år}: {verdi}")
    ds.plotly(
        create_bar_plot_with_button(
            [
                preppede_data["unike_bedrifter_per_år"],
                preppede_data["unike_bedrifter_per_kvartal"],
                preppede_data["unike_bedrifter_per_måned"],
                preppede_data["unike_bedrifter_per_uke"],
                preppede_data["unike_bedrifter_per_dag"],
            ],
            labels=["År", "Kvartal", "Måned", "Uke", "Dag"],
            default_active=2,
            xrangeslider=1,
            yaxis_title="Antall unike virksomheter",
        )
    )
    ds.header(content="Kumulativt histogram av unike virksomheter")
    første_dag_per_år, all_days = preppede_data["unike_bedrifter_første_dag_per_år"]
    ds.plotly(
        create_cumulative_histogram(
            data_frame=første_dag_per_år,
            x_col="opprettet_daymonth",
            label_col="opprettet_year",
            xaxis=all_days,
            xaxis_title="Årets dag",
            yaxis_title="Antall unike virksomheter",
        )
    )
    ds.header(content="Leverte digitale IA-tjenester per tjeneste/applikasjon")
    ds.plotly(
        create_line_plot(
            preppede_data["per_applikasjon"], x="Måned", y="Antall", color="Tjeneste"
        )
    )
    ds.plotly(create_table(preppede_data["antall_applikasjon_tabell"]))
    ds.plotly(create_table(preppede_data["antall_applikasjon_tabell_siste_30_dager"]))
    ds.header("Informasjons- vs. interaksjonstjeneste i forebyggingsplan")
    ds.plotly(
        create_bar_plot_with_button(
            list_of_series=[
                100 * preppede_data["andel_form_av_tjeneste_plan"],
                preppede_data["antall_form_av_tjeneste_plan"],
            ],
            labels=["Prosentandel", "Antall"],
            xaxis_title="Form av tjeneste",
        )
    )
    ds.header(content="Fordeling antall ansatte")
    fordeling_antall_ansatte = preppede_data["fordeling_antall_ansatte"]
    ds.plotly(
        create_bar_plot_with_button(
            [
                fordeling_antall_ansatte[tjeneste]
                for tjeneste in fordeling_antall_ansatte.keys()
            ],
            labels=list(fordeling_antall_ansatte.keys()),
            yaxis_title="Antall ansatte",
        )
    )
    ds.header("Tilbakevendende brukere")
    ds.markdown(
        md="""
        Grafene viser antall og prosentandel av virksomheter som har fått levert digital 
        IA-tjeneste i gjeldende kvartal, og som samtidig fikk levert digital IA-tjeneste  
        kvartalet etter. Dette gir en indikasjon på hvor mange av virksomhetene som jobber 
        systematisk med IA. 
        """
    )
    ds.plotly(
        create_bar_plot_with_button(
            list_of_series=[
                preppede_data["tilbakevendende_brukere"].Prosentandel,
                preppede_data["tilbakevendende_brukere"].Antall,
            ],
            labels=["Prosentandel", "Antall"],
            xaxis_title="Kvartal",
        )
    )

    return ds


def plot_test(data: pd.DataFrame):
    return create_line_plot(
        data["per_applikasjon"], x="Måned", y="Antall", color="Tjeneste"
    )


def markdown_table_row(items: pd.Series) -> str:
    return "| ".join([f"{år} | {verdi} | \n" for år, verdi in items])


def plot_asd(data: pd.DataFrame):
    return create_bar_plot_with_button(
        [
            data["unike_bedrifter_per_år"],
            data["unike_bedrifter_per_kvartal"],
            data["unike_bedrifter_per_måned"],
            data["unike_bedrifter_per_uke"],
            data["unike_bedrifter_per_dag"],
        ],
        labels=["År", "Kvartal", "Måned", "Uke", "Dag"],
        default_active=2,
        xrangeslider=1,
        yaxis_title="Antall unike virksomheter",
    )


def plot_tjenester_per_applikasjon(data: pd.DataFrame) -> Figure:
    return create_line_plot(
        data["per_applikasjon"], x="Måned", y="Antall", color="Tjeneste"
    )


def antall_per_app_tabell_mnd(data: pd.DataFrame) -> Markdown:
    return create_table(
        data["antall_applikasjon_tabell"]
        .sort_values(by="Måned", ascending=False)
        .head(24)
    )


def antall_per_app_tabell_dager(data: pd.DataFrame) -> Markdown:
    return create_table(data["antall_applikasjon_tabell_siste_30_dager"])


def informasjon_vs_interaksjon(data: pd.DataFrame) -> Figure:
    return create_bar_plot_with_button(
        list_of_series=[
            100 * data["andel_form_av_tjeneste_plan"],
            data["antall_form_av_tjeneste_plan"],
        ],
        labels=["Prosentandel", "Antall"],
        xaxis_title="Form av tjeneste",
    )


def fordeling_antall_ansatte(data: pd.DataFrame) -> Figure:
    antall_ansatte = data["fordeling_antall_ansatte"]
    return create_bar_plot_with_button(
        [antall_ansatte[tjeneste] for tjeneste in antall_ansatte.keys()],
        labels=list(antall_ansatte.keys()),
        yaxis_title="Antall ansatte",
    )


def plot_tilbakevendende_brukere(data: pd.DataFrame) -> Figure:
    return create_bar_plot_with_button(
        list_of_series=[
            data["tilbakevendende_brukere"].Prosentandel,
            data["tilbakevendende_brukere"].Antall,
        ],
        labels=["Prosentandel", "Antall"],
        xaxis_title="Kvartal",
    )


def plot_antall_unike_virksomheter_kumulativt(data: pd.DataFrame) -> Figure:
    første_dag_per_år, all_days = data["unike_bedrifter_første_dag_per_år"]
    return create_cumulative_histogram(
        data_frame=første_dag_per_år,
        x_col="opprettet_daymonth",
        label_col="opprettet_year",
        xaxis=all_days,
        xaxis_title="Årets dag",
        yaxis_title="Antall unike virksomheter",
    )


def unike_virksomheter_per_år_bulletlist(data) -> str:
    return "\n".join(
        [f"- {år}: {verdi} " for år, verdi in data["unike_bedrifter_per_år"].items()]
    )


def unike_virksomheter_bulletlist(data):
    df = pd.DataFrame(data["unike_bedrifter_per_år"].reset_index())
    df.columns = ["År", "Unike bedrifter"]
    return create_table(df)
