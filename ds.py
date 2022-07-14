import plotly.express as px
import plotly.io as plio
from datastory.datastory import DataStory


def create_bar_plot(data, **kwargs) -> str:
    fig = px.bar(data, width=1300, height=600, **kwargs)
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
    ds.plotly(create_bar_plot(data["unike_bedrifter_per_måned"]["orgnr"]))
    ds.header(content="Per applikasjon")
    ds.plotly(
        create_bar_plot(data["per_applikasjon"].astype(str), x="Måned", y="Antall"))

    return ds
