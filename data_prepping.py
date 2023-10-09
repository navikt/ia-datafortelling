import pandas as pd
from datetime import datetime, timedelta
from logger import log


def prep_data(data: pd.DataFrame) -> {}:
    log.info("Prepping data...")
    leverte_iatjenester = (
        data.assign(
            opprettet_year=data["opprettet"].dt.year,
            opprettet_yearquarter=data["opprettet"].apply(
                lambda x: f"{x.year} Q{x.quarter}"
            ),
            opprettet_yearmonth=data["opprettet"].apply(
                lambda x: f"{x.year}/{x.month:02d}"
            ),
            opprettet_yearweek=data["opprettet"].apply(date_to_yearweek),
            opprettet_date=data["opprettet"].dt.date,
        )
        # Vi sorterer etter dato og form av tjeneste så vi beholder interaksjons over
        # informasjonstjeneste med bruk av "drop_duplicates".
        # Hver gang vi leverer en interaksjonstjeneste i forebygginsplan, leverer vi
        # også en informasjonstjeneste (vi må åpne et kort for å utføre oppgaver).
        .sort_values(by=["opprettet_date", "form_av_tjeneste"], ascending=[True, False])
        .drop_duplicates(subset=["orgnr", "kilde_applikasjon", "opprettet_date"])
        .reset_index()
    )

    result = {
        "unike_bedrifter_per_år": unike_bedrifter_per_år(leverte_iatjenester),
        "unike_bedrifter_per_kvartal": unike_bedrifter_per_kvartal(leverte_iatjenester),
        "unike_bedrifter_per_måned": unike_bedrifter_per_mnd(leverte_iatjenester),
        "unike_bedrifter_per_uke": unike_bedrifter_per_uke(leverte_iatjenester),
        "unike_bedrifter_per_dag": unike_bedrifter_per_dag(leverte_iatjenester),
        "unike_bedrifter_første_dag_per_år": unike_bedrifter_første_dag_per_år(
            leverte_iatjenester
        ),
        "per_applikasjon": per_applikasjon(leverte_iatjenester),
        "antall_applikasjon_tabell": antall_applikasjon_tabell(leverte_iatjenester),
        "antall_applikasjon_tabell_siste_30_dager": antall_applikasjon_tabell_siste_30_dager(
            leverte_iatjenester
        ),
        "antall_form_av_tjeneste_plan": count_per_form_av_tjeneste(
            leverte_iatjenester, "FOREBYGGINGSPLAN"
        ),
        "fordeling_antall_ansatte": fordeling_antall_ansatte(leverte_iatjenester),
        "andel_form_av_tjeneste_plan": count_per_form_av_tjeneste(
            leverte_iatjenester, "FOREBYGGINGSPLAN", andel=True
        ),
        "tilbakevendende_brukere": tilbakevendende_brukere(leverte_iatjenester),
    }
    log.info("Prepping data...Done")
    return result


def unike_bedrifter_per_år(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_year").nunique()["orgnr"]


def unike_bedrifter_per_kvartal(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_yearquarter").orgnr.nunique()


def unike_bedrifter_per_mnd(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_yearmonth").orgnr.nunique()


def unike_bedrifter_per_uke(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_yearweek").orgnr.nunique()


def unike_bedrifter_per_dag(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_date").orgnr.nunique()


def unike_bedrifter_første_dag_per_år(
    leverte_iatjenester: pd.DataFrame,
) -> pd.DataFrame:
    første_dag_per_år = (
        leverte_iatjenester.sort_values(by=["opprettet_date"], ascending=True)
        .drop_duplicates(subset=["orgnr", "opprettet_year"])
        .assign(
            opprettet_daymonth=leverte_iatjenester["opprettet"].apply(formater_dagmåned)
        )
        .filter(["opprettet_daymonth", "opprettet_year"])
    )

    # Define a common x-axis with all days in a year
    years = første_dag_per_år.opprettet_year.unique()
    all_days = (
        pd.date_range(
            datetime(years.min(), 1, 1), datetime(years.max(), 12, 31), freq="d"
        )
        .to_series()
        .apply(formater_dagmåned)
        .unique()
    )

    return første_dag_per_år, all_days


def per_applikasjon(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    antall_per_mnd = per_app_per_mnd(leverte_iatjenester)
    antall_per_mnd = antall_per_mnd[
        ["kilde_applikasjon", "opprettet_yearmonth", "orgnr"]
    ]
    antall_per_mnd.columns = ["Tjeneste", "Måned", "Antall"]

    return antall_per_mnd.astype({"Måned": str, "Tjeneste": str, "Antall": int})


def antall_applikasjon_tabell(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    antall_per_mnd = per_app_per_mnd(leverte_iatjenester)
    antall_per_mnd = antall_per_mnd[
        ["kilde_applikasjon", "opprettet_yearmonth", "orgnr"]
    ]
    antall_per_mnd.columns = ["Tjeneste", "Måned", "Antall"]

    tjenester = antall_per_mnd["Tjeneste"].unique()
    måneder = antall_per_mnd["Måned"].unique()

    tjeneste_dataframes = dict()
    for tjeneste, antall_per_mnd in antall_per_mnd.groupby(["Tjeneste"]):
        tjeneste_dataframes[tjeneste[0]] = antall_per_mnd.set_index("Måned")

    tabell = pd.DataFrame(index=måneder, columns=tjenester)

    for tjeneste in tjenester:
        tabell[tjeneste] = tjeneste_dataframes[tjeneste]["Antall"]
        tabell[tjeneste] = tabell[tjeneste].fillna(0).astype("int")

    # turn table upside down
    tabell = tabell[::-1]

    return tabell.sort_index(axis=1).reset_index().rename(columns={"index": "Måned"})


def antall_applikasjon_tabell_siste_30_dager(
    leverte_iatjenester: pd.DataFrame,
) -> pd.DataFrame:
    now = datetime.now()
    antall_per_dag = (
        leverte_iatjenester[leverte_iatjenester.opprettet > now - timedelta(days=30)]
        .groupby(["opprettet_date", "kilde_applikasjon"], as_index=False)
        .count()
    )
    antall_per_dag = antall_per_dag[["kilde_applikasjon", "opprettet_date", "orgnr"]]
    antall_per_dag.columns = ["Tjeneste", "Dag", "Antall"]

    tjenester = antall_per_dag["Tjeneste"].unique()
    dager = antall_per_dag["Dag"].unique()

    tjeneste_dataframes = dict()
    for tjeneste, antall_per_dag in antall_per_dag.groupby(["Tjeneste"]):
        tjeneste_dataframes[tjeneste[0]] = antall_per_dag.set_index("Dag")

    tabell = pd.DataFrame(index=dager, columns=tjenester)

    for tjeneste in tjenester:
        tabell[tjeneste] = tjeneste_dataframes[tjeneste]["Antall"]
        tabell[tjeneste] = tabell[tjeneste].fillna(0).astype("int")

    # turn table upside down
    tabell = tabell[::-1]

    return tabell.sort_index(axis=1).reset_index().rename(columns={"index": "Dag"})


def count_per_form_av_tjeneste(
    leverte_iatjenester: pd.DataFrame, tjeneste: str, andel=False
):
    filter_tjeneste = leverte_iatjenester.kilde_applikasjon == tjeneste
    return leverte_iatjenester[filter_tjeneste].form_av_tjeneste.value_counts(
        normalize=andel
    )


def tilbakevendende_brukere(leverte_iatjenester: pd.DataFrame):
    unike_per_kvartal = leverte_iatjenester.drop_duplicates(
        subset=["orgnr", "opprettet_yearquarter"]
    )

    kvartaler = unike_per_kvartal["opprettet_yearquarter"].unique()
    kvartaler_til_sammenlikning = [
        (kvartaler[k - 1], kvartaler[k]) for k in range(1, len(kvartaler))
    ]

    return pd.DataFrame(
        [
            andel_tilbakevendende(unike_per_kvartal, gjeldende_kvartal, neste_kvartal)
            for gjeldende_kvartal, neste_kvartal in kvartaler_til_sammenlikning
        ]
    ).set_index("Kvartal")


def fordeling_antall_ansatte(leverte_iatjenester: pd.DataFrame) -> dict:
    relevant_data = leverte_iatjenester[
        ["orgnr", "kilde_applikasjon", "antall_ansatte"]
    ]

    bins = [0, 5, 10, 20, 50, 100, 100000]
    labels = ["0-4", "5-9", "10-19", "20-49", "50-99", "100+"]

    resultat = dict()
    for tjeneste in relevant_data["kilde_applikasjon"].unique():
        data_for_enkelttjeneste = relevant_data[
            relevant_data["kilde_applikasjon"] == tjeneste
        ]

        resultat[tjeneste] = (
            pd.cut(
                x=data_for_enkelttjeneste["antall_ansatte"],
                bins=bins,
                labels=labels,
                include_lowest=True,
                right=True,
            )
            .value_counts()
            .reindex(labels)
        )

    return resultat


def andel_tilbakevendende(
    unike_per_kvartal: pd.DataFrame,
    gjeldende_kvartal: pd.Period,
    neste_kvartal: pd.Period,
) -> {}:
    brukere_gjeldende_kvartal = filtrer_på_kvartal(unike_per_kvartal, gjeldende_kvartal)
    brukere_neste_kvartal = filtrer_på_kvartal(unike_per_kvartal, neste_kvartal)

    tilbakevendende = unike_per_kvartal.query(
        "opprettet_yearquarter == @gjeldende_kvartal"
    )[brukere_gjeldende_kvartal.isin(brukere_neste_kvartal)]

    return {
        "Kvartal": gjeldende_kvartal,
        "Antall": len(tilbakevendende),
        "Prosentandel": round(
            len(tilbakevendende) / len(brukere_gjeldende_kvartal) * 100, 1
        ),
    }


def filtrer_på_kvartal(df: pd.DataFrame, kvartal: pd.Period) -> pd.Series:
    return df[df["opprettet_yearquarter"] == kvartal]["orgnr"]


def per_app_per_mnd(df: pd.DataFrame):
    return df.groupby(
        ["opprettet_yearmonth", "kilde_applikasjon"], as_index=False
    ).count()


def formater_dagmåned(date: pd.Series):
    return f"{date.day:02d}.{date.month:02d}"


def date_to_yearweek(date: datetime.date) -> str:
    year = date.year
    month = date.month
    week = int(date.strftime("%V"))

    if (month == 1) & (week >= 52):
        year -= 1
    elif (month == 12) & (week == 1):
        year += 1

    return f"{year} U{week:02d}"
