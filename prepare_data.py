import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    temp = data.copy()

    temp["opprettet_year"] = temp["opprettet"].dt.year
    temp["opprettet_month"] = temp["opprettet"].dt.month

    prepped = {
        "unike_bedrifter_per_år": temp.groupby("opprettet_year").nunique()["orgnr"],
        "unike_bedrifter_per_måned": temp.groupby(["opprettet_year", "opprettet_month"]).nunique().tail(12)
    }

    return prepped
