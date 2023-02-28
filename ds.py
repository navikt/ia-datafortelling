import plotly.express as px
import plotly.graph_objects as go
import plotly.io as plio
from datastory.datastory import DataStory


def create_bar_plot(data, **kwargs) -> str:
    fig = px.bar(data, width=1300, height=600, **kwargs)
    return plio.to_json(fig)


def create_line_plot(data, **kwargs) -> str:
    fig = px.line(data, width=1300, height=600, **kwargs)
    return plio.to_json(fig)


def create_bar_plot_with_button(data, x, y1, y2, **kwargs) -> str:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            visible=True,
            x=data[x],
            y=data[y1],
            name=y1,
            **kwargs
        )
    )

    fig.add_trace(
        go.Bar(
            visible=False,
            x=data[x],
            y=data[y2],
            name=y2,
            **kwargs
        )
    )

    # Add button
    fig.update_layout(
        width=1300,
        height=600,
        updatemenus=[
            dict(
                active=0,
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True, False]}],
                        label=y1,
                        method="update",
                    ),
                    dict(
                        args=[{"visible": [False, True]}],
                        label=y2,
                        method="update",
                    )
                ]),
                showactive=True,
                xanchor="left",
                yanchor="top",
                x=0,
                y=1.1,
            ),
        ]
    )

    return plio.to_json(fig)


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
        width=1300,
        height=800,
        barmode="overlay",
        bargap=0,
        **kwargs,
    )

    return plio.to_json(fig)


def create_table(data) -> str:
    headers = data.columns
    cells = []
    for header in headers:
        cells.append(data[header].tolist())

    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(headers),
                    fill_color="rgb(195, 0, 0)",
                    font=dict(color="white", size=12),
                    align="left",
                ),
                cells=dict(values=cells, align="left"),
            )
        ],
        layout=go.Layout(height=600),
    )

    return plio.to_json(fig)


def create_datastory(preppede_data: {}) -> DataStory:
    ds = DataStory(name="Leverte IA-tjenester")
    ds.header(content="Leverte digitale IA-tjenester")
    ds.markdown(
        md=f""" 
    Statistikken på denne siden viser antall digitale IA-tjenester. 
    Dataregistreringen startet mars 2021.
    
    En digital IA-tjeneste telles når en bruker har benyttet seg av innholdet i 
    tjenesten. Det er ikke tilstrekkelig at brukeren kun har besøkt forsiden.

    - 2021: {preppede_data["unike_bedrifter_per_år"][2021]}
    - 2022: {preppede_data["unike_bedrifter_per_år"][2022]}
    - 2023: {preppede_data["unike_bedrifter_per_år"][2023]}
    
    Vi har hatt en feil på telling av digitale IA-tjenester i perioden 19. mai 
    til 1. juli 2022. Det er ca 1000 digitale IA-tjenester som ikke er kommet 
    med i statistikken.
                
    """
    )
    ds.header(content="Unike virksomheter siste 12 måneder")
    ds.plotly(create_bar_plot(preppede_data["unike_bedrifter_per_måned"]))
    ds.header(content="Kumulativt histogram av unike virksomheter")
    første_dag_per_år, all_days = preppede_data["unike_bedrifter_første_dag_per_år"]
    ds.plotly(create_cumulative_histogram(
        data_frame=første_dag_per_år,
        x_col="opprettet_daymonth",
        label_col="opprettet_year",
        xaxis=all_days,
        xaxis_title="Årets dag",
        yaxis_title="Antall unike virksomheter",
    ))
    ds.header(content="Leverte digitale IA-tjenester per tjeneste/applikasjon")
    ds.plotly(
        create_line_plot(
            preppede_data["per_applikasjon"], x="Måned", y="Antall", color="Tjeneste"
        )
    )
    ds.plotly(create_table(preppede_data["antall_applikasjon_tabell"]))
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
            preppede_data["tilbakevendende_brukere"], x="Kvartal", y1="Prosentandel", y2="Antall",
        )
    )

    return ds
