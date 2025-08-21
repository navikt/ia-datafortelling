from typing import Any

import pandas as pd
from google.cloud.bigquery import Client
from google.cloud.bigquery.job import QueryJob


def query_data(
    project: str,
    dataset: str,
    table: str,
    limit: str | None = None,
) -> pd.DataFrame:
    query = f"SELECT  * FROM `{project}.{dataset}.{table}`"
    client = Client(project)
    query = query + ("" if limit is None else f" LIMIT {limit}")
    query_job = client.query(query)

    return pd.DataFrame(data=format_results(query_job=query_job))


def format_results(query_job: QueryJob) -> list[dict[str, Any]]:
    results = query_job.result()
    return [{key: value for key, value in row.items()} for row in results]
