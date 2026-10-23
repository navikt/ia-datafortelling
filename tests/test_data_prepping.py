import pandas as pd

from leverte_ia_tjenester.data_prepping import prep_data


def test_prep_data_summarizes_two_quarters_and_returning_orgs():
    data = pd.DataFrame(
        {
            "orgnr": ["100", "101", "100"],
            "opprettet": pd.to_datetime(
                ["2024-01-15", "2024-01-20", "2024-04-10"]
            ),
            "antall_ansatte": [3, 8, 3],
        }
    )

    result = prep_data(data)

    assert result["unike_bedrifter_per_kvartal"].to_dict() == {
        "2024 Q1": 2,
        "2024 Q2": 1,
    }
    assert result["tilbakevendende_brukere"].loc["2024 Q1", "Antall"] == 1
