import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    cleaned = data.copy()

    cleaned["opprettet_year"] = cleaned["opprettet"].dt.year
    cleaned["opprettet_month"] = cleaned["opprettet"].dt.month
    cleaned["opprettet_date"] = cleaned["opprettet"].dt.date

    cleaned = cleaned.drop_duplicates(
        subset=["orgnr", "kilde_applikasjon", "opprettet_date"]
    ).sort_values(by=["opprettet_date"])

    prepped = {
        "unike_bedrifter_per_år": unike_bedrifter_per_år(cleaned),
        "unike_bedrifter_per_måned": unike_bedrifter_per_mnd(cleaned),
        "per_applikasjon": per_applikasjon(cleaned),
        "antall_applikasjon_tabell": antall_applikasjon_tabell(cleaned)
    }

    return prepped


def unike_bedrifter_per_år(cleaned: pd.DataFrame) -> pd.DataFrame:
    return cleaned.groupby("opprettet_year").nunique()["orgnr"]


def unike_bedrifter_per_mnd(cleaned: pd.DataFrame) -> pd.DataFrame:
    siste_12_måneder = (
        cleaned.groupby(["opprettet_year", "opprettet_month"]).nunique().tail(12)
    )
    siste_12_måneder.index = siste_12_måneder.index.map(
        lambda multi_index: "{}/{}".format(multi_index[0], multi_index[1])
    )
    return siste_12_måneder["orgnr"]


def per_applikasjon(cleaned: pd.DataFrame) -> pd.DataFrame:
    per_app = cleaned.groupby(
        ["opprettet_year", "opprettet_month", "kilde_applikasjon"], as_index=False
    ).count()
    per_app["Måned"] = (
        per_app["opprettet_month"].astype(str)
        + "/"
        + per_app["opprettet_year"].astype(str)
    )
    per_app = per_app[["kilde_applikasjon", "Måned", "orgnr"]]
    per_app.columns = ["Tjeneste", "Måned", "Antall"]

    return per_app.astype({"Måned": str, "Tjeneste": str, "Antall": int})


def antall_applikasjon_tabell(cleaned: pd.DataFrame) -> pd.DataFrame:
    per_app = cleaned.groupby(
        ["opprettet_year", "opprettet_month", "kilde_applikasjon"], as_index=False
    ).count()
    per_app["Måned"] = (
        per_app["opprettet_month"].astype(str)
        + "/"
        + per_app["opprettet_year"].astype(str)
    )
    per_app = per_app[["kilde_applikasjon", "Måned", "orgnr"]]
    per_app.columns = ["Tjeneste", "Måned", "Antall"]

    tjenester = per_app["Tjeneste"].unique()
    måneder = per_app["Måned"].unique()

    tjeneste_dataframes = dict()
    for tjeneste, df in per_app.groupby(["Tjeneste"]):
        tjeneste_dataframes[tjeneste] = df.set_index("Måned")

    tabell = pd.DataFrame(index=måneder, columns=tjenester)

    for tjeneste in tjenester:
        tabell[tjeneste] = tjeneste_dataframes[tjeneste]["Antall"]
        tabell[tjeneste] = tabell[tjeneste].fillna(0).astype("int")

    tabell.reset_index(inplace=True)
    tabell = tabell.rename(columns={"index": "MÅNED"})

    return tabell
