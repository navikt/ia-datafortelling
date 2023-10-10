import pandas as pd
from IPython.core.display import Markdown
from plotly.graph_objs import Figure

from visualization_utils import create_line_plot, create_bar_plot_with_button, create_cumulative_histogram, create_table


def plot_unike_bedrifter(data: pd.DataFrame):
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


def tabell_antall_per_app_siste_24_mnd(data: pd.DataFrame) -> Markdown:
    return create_table(
        data["antall_applikasjon_tabell"]
        .sort_values(by="Måned", ascending=False)
        .head(24)
    )


def tabell_antall_per_app_siste_30_dager(data: pd.DataFrame) -> Markdown:
    return create_table(data["antall_applikasjon_tabell_siste_30_dager"])


def plot_informasjon_vs_interaksjon(data: pd.DataFrame) -> Figure:
    return create_bar_plot_with_button(
        list_of_series=[
            100 * data["andel_form_av_tjeneste_plan"],
            data["antall_form_av_tjeneste_plan"],
        ],
        labels=["Prosentandel", "Antall"],
        xaxis_title="Form av tjeneste",
    )


def plot_fordeling_antall_ansatte(data: pd.DataFrame) -> Figure:
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


def unike_virksomheter_bulletlist(data):
    df = pd.DataFrame(data["unike_bedrifter_per_år"].reset_index())
    df.columns = ["År", "Unike bedrifter"]
    return create_table(df)
