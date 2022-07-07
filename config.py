from enum import Enum

PROJECT = "teampam-prod-7da6"

DATASET = "metrics"

TABLE = "brukernotifikasjoner"

SQL_QUERY = f"SELECT  * FROM `{PROJECT}.{DATASET}.{TABLE}`"

DATASTORY_PROD = "https://nada.intern.nav.no/api"


class DataInColumns(Enum):
    YEAR = "year"
    WEEK = "week"
    COUNT = "count"
    TIMESTAMP = "timestamp"
    STATUS = "status"


class DataNewColumns(Enum):
    YEAR_CORRECTED = "year_corrected"
    WEEK_CORRECTED = "week_corrected"
    LOADED_DAY = "loaded_date"
    LOADED_DAY_STR = "loaded_date_str"
    FIRST_DAY_OF_WEEK = "first_day_of_week"
    FORMATTED_WEEK = "week_formatted"

