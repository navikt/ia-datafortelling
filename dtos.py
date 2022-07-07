import datetime

from typing import Dict, Any
from dataclasses import dataclass, field


@dataclass
class BrukerNotifikasjonerMetric:
    year: int
    week: int
    count: int
    status: str
    timestamp: int = field(init=False)

    def __post_init__(self):
        self.timestamp = round(datetime.datetime.now().timestamp())

    def prep(self) -> Dict[str, Any]:
        return self.__dict__

    @classmethod
    def from_dict(cls, row: Dict[str, Any]):
        return BrukerNotifikasjonerMetric(**row)


@dataclass
class BrukerNotifikasjonerPrep:
    year: int
    week: int
    count: int
    timestamp: int
    status: int
    correct: bool = True

    def __post_init__(self):
        self.loaded_date = datetime.date.fromtimestamp(self.timestamp)
        self.loaded_date_str = self.loaded_date.strftime("%d-%m-%Y")

        self.year_corrected, self.week_corrected = self._correct_week(year=self.year,
                                                                      week=self.week,
                                                                      correct=self.correct)

        self.first_day_of_week = self._date_from_week(year=self.year_corrected, week=self.week_corrected)
        self.week_formatted = self._format_year_week(year=self.year_corrected, week=self.week_corrected)

    def to_dict(self) -> dict:
        return {key: value for key, value in self.__dict__.items() if key != "correct"}

    @staticmethod
    def _correct_week(year: int, week: int, correct: bool = True) -> tuple:  # [int, int]:
        corrected_year = year
        corrected_week = week

        if correct:
            if corrected_week >= 53:
                corrected_year -= 1

        return corrected_year, corrected_week

    @staticmethod
    def _date_from_week(year: int, week: int) -> datetime.date:
        return datetime.datetime.strptime(f"{year} {week} 1", "%Y %W %w").date()

    @staticmethod
    def _format_year_week(year: int, week: int) -> str:
        return f"{year} U{week}"
