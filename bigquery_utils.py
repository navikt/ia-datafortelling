from typing import List, Dict, Any

import pandas as pd
from google.cloud.bigquery import Client
from google.cloud.bigquery.job import QueryJob

import config


def create_client() -> Client:
    client = Client(project=config.PROJECT)
    return client


def execute_query(client: Client, query: str) -> QueryJob:
    query_job = client.query(query=query)
    return query_job


def format_results(query_job: QueryJob) -> List[Dict[str, Any]]:
    results = query_job.result()
    return [{key: value for key, value in row.items()} for row in results]


def query_dataframe(client: Client, query: str) -> pd.DataFrame:
    query_job = execute_query(client=client, query=query)
    return pd.DataFrame(data=format_results(query_job=query_job))
