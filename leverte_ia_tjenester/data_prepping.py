from datetime import datetime

import pandas as pd
from pandas import DataFrame


def prep_data(data: pd.DataFrame) -> {}:
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
        .sort_values(by=["opprettet_date"], ascending=[True])
        .drop_duplicates(subset=["orgnr", "opprettet_date"])
        .reset_index()
    )

    return {
        "unike_bedrifter_per_år": unike_bedrifter_per_år(leverte_iatjenester),
        "unike_bedrifter_per_kvartal": unike_bedrifter_per_kvartal(leverte_iatjenester),
        "unike_bedrifter_per_måned": unike_bedrifter_per_mnd(leverte_iatjenester),
        "unike_bedrifter_per_uke": unike_bedrifter_per_uke(leverte_iatjenester),
        "unike_bedrifter_per_dag": unike_bedrifter_per_dag(leverte_iatjenester),
        "unike_bedrifter_første_dag_per_år": unike_bedrifter_første_dag_per_år(
            leverte_iatjenester
        ),
        "fordeling_antall_ansatte": fordeling_antall_ansatte(leverte_iatjenester),
        "tilbakevendende_brukere": tilbakevendende_brukere(leverte_iatjenester),
    }


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
) -> tuple[DataFrame, pd.DatetimeIndex]:
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
        ["orgnr", "antall_ansatte"]
    ]

    bins = [0, 5, 10, 20, 50, 100, 100000]
    labels = ["0-4", "5-9", "10-19", "20-49", "50-99", "100+"]

    return (pd.cut(
            x=relevant_data["antall_ansatte"],
            bins=bins,
            labels=labels,
            include_lowest=True,
            right=True,
        )
            .value_counts()
            .reindex(labels))


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
