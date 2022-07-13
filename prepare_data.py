import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    temp = data.copy()

    temp["opprettet_year"] = temp["opprettet"].dt.year
    temp["opprettet_month"] = temp["opprettet"].dt.month

    prepped = {
        "unike_bedrifter_per_år": temp.groupby("opprettet_year").nunique()["orgnr"]
    }

    return prepped
