from typing import List, Dict, Any

import pandas as pd
from google.cloud.bigquery import Client
from google.cloud.bigquery.job import QueryJob

PROJECT = "teamia-prod-df3d"
DATASET = "ia_tjenester_metrikker"
TABLE = "IA-tjenester-metrikker"

SQL_QUERY = f"SELECT  * FROM `{PROJECT}.{DATASET}.{TABLE}`"


def query_data(limit=None) -> [pd.DataFrame]:
    client = Client(project=PROJECT)
    query = SQL_QUERY + ("" if limit is None else f" LIMIT {limit}")
    query_job = client.query(query)

    return pd.DataFrame(data=format_results(query_job=query_job))


def format_results(query_job: QueryJob) -> List[Dict[str, Any]]:
    results = query_job.result()
    return [{key: value for key, value in row.items()} for row in results]
