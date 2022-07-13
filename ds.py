import pandas as pd
import plotly.express as px
import plotly.io as plio
from datastory.datastory import DataStory

from config import DataNewColumns, DataInColumns


def create_bar_plot(data: pd.DataFrame) -> str:
    max_value = (
        data[
            [
                DataNewColumns.LOADED_DAY_STR.value,
                DataNewColumns.FORMATTED_WEEK.value,
                DataInColumns.COUNT.value,
            ]
        ]
        .groupby(
            by=[
                DataNewColumns.LOADED_DAY_STR.value,
                DataNewColumns.FORMATTED_WEEK.value,
            ]
        )
        .sum()
        .reset_index(drop=False)
    )[DataInColumns.COUNT.value].max()

    fig = px.bar(
        data,
        x=DataNewColumns.FORMATTED_WEEK.value,
        y=DataInColumns.COUNT.value,
        animation_frame=DataNewColumns.LOADED_DAY_STR.value,
        color=DataInColumns.STATUS.value,
        custom_data=[DataNewColumns.LOADED_DAY_STR.value, DataInColumns.STATUS.value],
        width=1300,
        height=600,
    )

    fig["layout"]["sliders"][0]["currentvalue"]["prefix"] = "Dag rapportert: "
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "<b>Uke:</b> %{x}",
                "<b>Antall:</b> %{y}",
                "<b>Dag rapportert:</b> %{customdata[0]}",
                "<b>Status:</b> %{customdata[1]}",
                "<extra></extra>",
            ]
        )
    )
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(range=[0, 1.2 * max_value])
    fig.update_layout(yaxis_title="Antall", xaxis_title="Dag")

    return plio.to_json(fig)


def create_datastory(data: {}):
    ds = DataStory(name="Leverte IA-tjenester")
    ds.header(content="Unike bedrifter per år")
    ds.markdown(
        md=f""" 
    Statistikken på denne siden viser antall digitale IA-tjenester. 
    Dataregistreringen startet mars 2021.
    
    En digital IA-tjeneste telles når en bruker har benyttet seg av innholdet i 
    tjenesten. Det er ikke tilstrekkelig at brukeren kun har besøkt forsiden.

    Vi har hatt en feil på telling av digitale IA-tjenester i perioden 19. mai 
    til 1. juli 2022. Det er ca 1000 digitale IA-tjenester som ikke er kommet 
    med i statistikken.
                
    - 2021: {data["unike_bedrifter_per_år"][2021]}
    - 2022: {data["unike_bedrifter_per_år"][2022]}
    """
    )
    ds.header(content="Unike bedrifter siste 12 måneder")
    ds.plotly(plio.to_json(px.bar(data["unike_bedrifter_per_måned"]["orgnr"], width=1300, height=600)))

    return ds


def create_datastory_pam(data: pd.DataFrame) -> DataStory:
    ds = DataStory(name="arbeidsplassen.no brukernotifikasjoner metrikker")

    ds.header(content="Om denne datafortellingen")
    ds.markdown(
        md="""Denne datafortellingen illustrerer hvor mange brukernotifikasjoner arbeidsplassen.no har sendt ut og 
    vist bruker på Ditt NAV og hvor mange av de som er utført av bruker."""
    )

    ds.header(content="""Oversikt over utsendte og oppfylte meldinger om CV""")
    ds.markdown(
        md="""Denne grafen viser hvor mange nyregistrerte i NAV som har fått beskjed om å legge inn eller 
    oppdatere CV-en sin, og hvor mange av de som har gjort det. Hvis en bruker går ut av oppfølging, før CV er lagt inn 
    eller oppdatert så vises dette også i grafen."""
    )

    fig = create_bar_plot(data=data)
    ds.plotly(fig=fig)
    ds.markdown(
        md="""Ved å bevege «slideren» i bunn av grafen, kan du bestemme fra hvilket tidspunkt du ønsker å 
    se status for."""
    )

    ds.header(content="Beskrivelse av statuser")
    ds.markdown(
        md="""
- **cvOppdatert**: Er varslet, har oppdatert og varslet har blitt fjernet.
- **ikkeUnderOppfølging**: Ikke oppdatert, men heller ikke nødvendig. Er ikke under oppfølging lengere.
- **varslet**: under oppfølging og har ikke oppdatert CVen."""
    )

    return ds
