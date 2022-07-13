import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    temp = data.copy()

    temp["opprettet_year"] = temp["opprettet"].dt.year
    temp["opprettet_month"] = temp["opprettet"].dt.month

    siste_12_måneder = temp.groupby(["opprettet_year", "opprettet_month"]).nunique().tail(12)
    siste_12_måneder.index = siste_12_måneder.index.map(lambda multi_index: "{}/{}".format(multi_index[0], multi_index[1]))

    prepped = {
        "unike_bedrifter_per_år": temp.groupby("opprettet_year").nunique()["orgnr"],
        "unike_bedrifter_per_måned": siste_12_måneder
    }

    return prepped
