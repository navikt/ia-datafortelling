from datetime import timedelta


def calculate_key_metrics(data_raw, startdato, sluttdato):
    data = (
        data_raw[data_raw.kilde_applikasjon == "FOREBYGGINGSPLAN"]
        .assign(opprettet_date=data_raw["opprettet"].dt.date)
        .sort_values(by=["orgnr", "opprettet"])
        .drop_duplicates(subset=["orgnr", "opprettet_date"])
    )
    antall_dager_per_orgnr = data[
        (data.opprettet > startdato) & (data.opprettet <= sluttdato)
        ].orgnr.value_counts()

    antall_åpnet_kort = antall_dager_per_orgnr.count()
    antall_åpnet_kort_flere_dager = (antall_dager_per_orgnr >= 2).sum()

    return antall_åpnet_kort, antall_åpnet_kort_flere_dager


def calculate_repeated_key_metrics(
        data_raw,
        startdato,
        sluttdato,
        minimum_days_between_visits=30,
        kilde_applikasjon="FOREBYGGINGSPLAN",
):
    applikasjon_data = data_raw[
        data_raw.kilde_applikasjon == kilde_applikasjon
        ].sort_values(by=["opprettet"])
    datofiltrert_data = applikasjon_data[
        (applikasjon_data.opprettet > startdato)
        & (applikasjon_data.opprettet <= sluttdato)
        ]
    only_duplicated_data = datofiltrert_data[
        datofiltrert_data.duplicated("orgnr", keep=False)
    ]

    first_date_set = only_duplicated_data.drop_duplicates(
        subset=["orgnr"], keep="first"
    )
    last_date_set = only_duplicated_data.drop_duplicates(subset=["orgnr"], keep="last")

    combined_set = first_date_set.merge(last_date_set, on="orgnr")
    diffed_set = combined_set.assign(
        diff=(combined_set["opprettet_y"] - combined_set["opprettet_x"])
    )

    filtered_set = diffed_set[
        diffed_set["diff"] > timedelta(days=minimum_days_between_visits)
        ]

    return filtered_set.orgnr.size