import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    cleaned = data.copy()

    cleaned["opprettet_year"] = cleaned["opprettet"].dt.year
    cleaned["opprettet_month"] = cleaned["opprettet"].dt.month
    cleaned["opprettet_dato"] = cleaned["opprettet"].dt.date

    cleaned = cleaned.drop_duplicates(
        subset=["orgnr", "kilde_applikasjon", "opprettet_dato"]
    ).sort_values(by=["opprettet_dato"])

    prepped = {
        "unike_bedrifter_per_år": unike_bedirfter_per_år(cleaned),
        "unike_bedrifter_per_måned": unike_bedrifter_per_mnd(cleaned),
        "per_tjeneste": per_tjeneste(cleaned),
    }

    return prepped


def unike_bedirfter_per_år(cleaned):
    return cleaned.groupby("opprettet_year").nunique()["orgnr"]


def unike_bedrifter_per_mnd(cleaned):
    siste_12_måneder = (
        cleaned.groupby(["opprettet_year", "opprettet_month"]).nunique().tail(12)
    )
    siste_12_måneder.index = siste_12_måneder.index.map(
        lambda multi_index: "{}/{}".format(multi_index[0], multi_index[1])
    )
    return siste_12_måneder["orgnr"]


def per_tjeneste(temp):
    per_app = temp.groupby(
        ["kilde_applikasjon", "opprettet_year", "opprettet_month"], as_index=False
    ).count()
    per_app["Tid"] = (
        per_app["opprettet_month"].astype(str)
        + "/"
        + per_app["opprettet_year"].astype(str)
    )
    per_app = per_app[["kilde_applikasjon", "Tid", "orgnr"]]
    per_app.columns = ["Tjeneste", "Tid", "Antall"]

    return per_app.astype({"Tid": str, "Tjeneste": str, "Antall": int})
