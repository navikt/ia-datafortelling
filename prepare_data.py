import datetime

from typing import List, Dict

import pandas as pd

from config import DataNewColumns, DataInColumns
from dtos import BrukerNotifikasjonerPrep


def fill_missing_weeks(data: pd.DataFrame) -> pd.DataFrame:
    missing_data = []
    all_weeks = set(data[DataNewColumns.FORMATTED_WEEK.value].unique())
    all_status = data[DataInColumns.STATUS.value].unique()

    for timestamp in data[DataInColumns.TIMESTAMP.value].unique():
        current_data = data[data[DataInColumns.TIMESTAMP.value] == timestamp]
        current_weeks = set(current_data[DataNewColumns.FORMATTED_WEEK.value].unique())

        diffs = list(all_weeks.difference(current_weeks))

        missing_data.extend([BrukerNotifikasjonerPrep(status=status,
                                                      count=0,
                                                      timestamp=timestamp,
                                                      year=int(diff[:4]),
                                                      week=int(diff[6:]),
                                                      correct=False
                                                      ).to_dict() for status in all_status for diff in diffs])

    return pd.DataFrame(data=missing_data)


def filter_data(data: pd.DataFrame) -> pd.DataFrame:
    return data[(data[DataNewColumns.LOADED_DAY.value] >= datetime.date(year=2021, month=12, day=3)) &
                (data[DataNewColumns.FIRST_DAY_OF_WEEK.value] >= datetime.date(year=2021, month=9, day=1))]


def prep_data(data: List[Dict]) -> pd.DataFrame:
    data_rows = [BrukerNotifikasjonerPrep(year=row[DataInColumns.YEAR.value],
                                          week=row[DataInColumns.WEEK.value],
                                          timestamp=row[DataInColumns.TIMESTAMP.value],
                                          status=row[DataInColumns.STATUS.value],
                                          count=row[DataInColumns.COUNT.value]).to_dict() for row in data]

    data = pd.DataFrame(data=data_rows)
    filtered_data = filter_data(data=data)

    missing_data = fill_missing_weeks(data=filtered_data)

    prepped_data = filtered_data.append(missing_data)

    return prepped_data.sort_values(by=[DataNewColumns.LOADED_DAY.value, DataNewColumns.FIRST_DAY_OF_WEEK.value])
