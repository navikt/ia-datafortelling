import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    temp = data.copy()

    temp["opprettet_year"] = temp["opprettet"].dt.year
    temp["opprettet_month"] = temp["opprettet"].dt.month
    temp["opprettet_dato"] = temp["opprettet"].dt.date

    temp = temp.drop_duplicates(subset=["orgnr", "kilde_applikasjon", "opprettet_dato"])

    siste_12_måneder = (
        temp.groupby(["opprettet_year", "opprettet_month"]).nunique().tail(12)
    )
    siste_12_måneder.index = siste_12_måneder.index.map(
        lambda multi_index: "{}/{}".format(multi_index[0], multi_index[1])
    )

    per_app = temp.groupby(
        ["kilde_applikasjon", "opprettet_year", "opprettet_month"], as_index=False
    ).count()[["kilde_applikasjon", "opprettet_year", "opprettet_month", "orgnr"]]
    per_app.columns = ["Tjeneste", "År", "Måned", "Antall"]

    prepped = {
        "unike_bedrifter_per_år": temp.groupby("opprettet_year").nunique()["orgnr"],
        "unike_bedrifter_per_måned": siste_12_måneder,
        "per_applikasjon": per_app,
    }

    return prepped
