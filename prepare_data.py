import pandas as pd


def prep_data(data: pd.DataFrame) -> {}:
    leverte_iatjenester = (
        data.assign(opprettet_year=data["opprettet"].dt.year)
        .assign(opprettet_month=data["opprettet"].dt.month)
        .assign(opprettet_date=data["opprettet"].dt.date)
        .drop_duplicates(subset=["orgnr", "kilde_applikasjon", "opprettet_date"])
        .sort_values(by=["opprettet_date"])
        .reset_index()
    )

    return {
        "unike_bedrifter_per_år": unike_bedrifter_per_år(leverte_iatjenester),
        "unike_bedrifter_per_måned": unike_bedrifter_per_mnd(leverte_iatjenester),
        "per_applikasjon": per_applikasjon(leverte_iatjenester),
        "antall_applikasjon_tabell": antall_applikasjon_tabell(leverte_iatjenester),
        "tilbakevendende_brukere": tilbakevendende_brukere(leverte_iatjenester),
    }


def unike_bedrifter_per_år(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    return leverte_iatjenester.groupby("opprettet_year").nunique()["orgnr"]


def unike_bedrifter_per_mnd(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    siste_12_måneder = (
        leverte_iatjenester.groupby(["opprettet_year", "opprettet_month"])
        .nunique()
        .tail(12)
    )
    siste_12_måneder.index = siste_12_måneder.index.map(
        lambda multi_index: "{}/{}".format(multi_index[0], multi_index[1])
    )
    return siste_12_måneder["orgnr"]


def per_applikasjon(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    antall_per_mnd = per_app_per_mnd(leverte_iatjenester).assign()
    antall_per_mnd["Måned"] = formater_måned(antall_per_mnd)
    antall_per_mnd = antall_per_mnd[["kilde_applikasjon", "Måned", "orgnr"]]
    antall_per_mnd.columns = ["Tjeneste", "Måned", "Antall"]

    return antall_per_mnd.astype({"Måned": str, "Tjeneste": str, "Antall": int})


def antall_applikasjon_tabell(leverte_iatjenester: pd.DataFrame) -> pd.DataFrame:
    antall_per_mnd = per_app_per_mnd(leverte_iatjenester)
    antall_per_mnd["Måned"] = formater_måned(antall_per_mnd)
    antall_per_mnd = antall_per_mnd[["kilde_applikasjon", "Måned", "orgnr"]]
    antall_per_mnd.columns = ["Tjeneste", "Måned", "Antall"]

    tjenester = antall_per_mnd["Tjeneste"].unique()
    måneder = antall_per_mnd["Måned"].unique()

    tjeneste_dataframes = dict()
    for tjeneste, antall_per_mnd in antall_per_mnd.groupby(["Tjeneste"]):
        tjeneste_dataframes[tjeneste] = antall_per_mnd.set_index("Måned")

    tabell = pd.DataFrame(index=måneder, columns=tjenester)

    for tjeneste in tjenester:
        tabell[tjeneste] = tjeneste_dataframes[tjeneste]["Antall"]
        tabell[tjeneste] = tabell[tjeneste].fillna(0).astype("int")

    return tabell.reset_index().rename(columns={"index": "MÅNED"})


def tilbakevendende_brukere(leverte_iatjenester: pd.DataFrame):
    unike_per_kvartal = leverte_iatjenester.assign(
        kvartal=pd.PeriodIndex(leverte_iatjenester["opprettet"], freq="Q")
    ).drop_duplicates(subset=["orgnr", "kvartal"])

    kvartaler = unike_per_kvartal["kvartal"].unique()
    kvartaler_til_sammenlikning = [
        (kvartaler[k - 1], kvartaler[k]) for k in range(1, len(kvartaler))
    ]

    return pd.DataFrame(
        [
            andel_tilbakevendende(unike_per_kvartal, forrige_kvartal, gjeldende_kvartal)
            for forrige_kvartal, gjeldende_kvartal in kvartaler_til_sammenlikning
        ],
        columns=["Kvartal", "Prosentandel"],
    )


def andel_tilbakevendende(
    unike_per_kvartal: pd.DataFrame,
    forrige_kvartal: pd.Period,
    gjeldende_kvartal: pd.Period,
) -> ():
    brukere_forrige_kvartal = filtrer_på_kvartal(unike_per_kvartal, forrige_kvartal)
    brukere_dette_kvartalet = filtrer_på_kvartal(unike_per_kvartal, gjeldende_kvartal)

    tilbakevendende = unike_per_kvartal.query("kvartal == @gjeldende_kvartal")[
        brukere_dette_kvartalet.isin(brukere_forrige_kvartal)
    ]

    return (
        formater_kvartal(gjeldende_kvartal),
        len(tilbakevendende) / len(brukere_dette_kvartalet) * 100,
    )


def filtrer_på_kvartal(df: pd.DataFrame, kvartal: pd.Period) -> pd.Series:
    return df[df["kvartal"] == kvartal]["orgnr"]


def per_app_per_mnd(df: pd.DataFrame):
    return df.groupby(
        ["opprettet_year", "opprettet_month", "kilde_applikasjon"], as_index=False
    ).count()


def formater_måned(df: pd.DataFrame):
    return df["opprettet_month"].astype(str) + "/" + df["opprettet_year"].astype(str)


def formater_kvartal(kvartal: pd.Period):
    return str(kvartal.year) + " Q" + str(kvartal.quarter)
