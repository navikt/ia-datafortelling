import plotly.express as px
import plotly.io as plio
import plotly.graph_objects as go
from datastory.datastory import DataStory


def create_bar_plot(data, **kwargs) -> str:
    fig = px.bar(data, width=1300, height=600, **kwargs)
    return plio.to_json(fig)

def create_table(data) -> str:
    headers = data.columns
    cells = []
    for header in headers:
        cells.append(data[header].tolist())

    fig = go.Figure(
        data=[go.Table(
            header=dict(
                values=list(headers),
                fill_color='rgb(195, 0, 0)',
                font=dict(color='white', size=12),
                align='left'),
            cells=dict(
                values=cells,
                align='left'
            )
        )],
        layout=go.Layout(height=600)
    )

    return plio.to_json(fig)



def create_datastory(preppede_data: {}) -> DataStory:
    ds = DataStory(name="Leverte IA-tjenester")
    ds.header(content="Leverte digitale IA-tjenester TEST")
    ds.markdown(
        md=f""" 
    Statistikken på denne siden viser antall digitale IA-tjenester. 
    Dataregistreringen startet mars 2021.
    
    En digital IA-tjeneste telles når en bruker har benyttet seg av innholdet i 
    tjenesten. Det er ikke tilstrekkelig at brukeren kun har besøkt forsiden.

    Vi har hatt en feil på telling av digitale IA-tjenester i perioden 19. mai 
    til 1. juli 2022. Det er ca 1000 digitale IA-tjenester som ikke er kommet 
    med i statistikken.
                
    - 2021: {preppede_data["unike_bedrifter_per_år"][2021]}
    - 2022: {preppede_data["unike_bedrifter_per_år"][2022]}
    """
    )
    ds.header(content="Unike bedrifter siste 12 måneder")
    ds.plotly(create_bar_plot(preppede_data["unike_bedrifter_per_måned"]))
    ds.header(content="Per tjeneste/applikasjon graf")
    ds.plotly(
        create_bar_plot(
            preppede_data["per_applikasjon"], x="Måned", y="Antall", color="Tjeneste"
        )
    )
    ds.header(content="Per tjeneste/applikasjon tabell")
    ds.plotly(create_table(preppede_data["antall_applikasjon_tabell"]))

    return ds
