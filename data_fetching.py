from typing import List, Dict, Any

import config
import pandas as pd
import logging
from google.cloud.bigquery import Client
from google.cloud.bigquery.job import QueryJob


logger = logging.get_logger()


def query_dataframe(client: Client, query: str) -> pd.DataFrame:
    query_job = execute_query(client=client, query=query)
    return pd.DataFrame(data=format_results(query_job=query_job))


def query_data(sqlClient, limit=None) -> [pd.DataFrame]:
    logger.info("Querying data...")
    data = query_dataframe(
        client=sqlClient,
        query=config.SQL_QUERY + ("" if limit is None else f" LIMIT {limit}"),
    )
    logger.info("Querying data...Done")
    return data


def create_client() -> Client:
    logger.info("Creating BigQuery client...")
    client = Client(project=config.PROJECT)
    logger.info("Creating BigQuery client...Done")
    return client


def execute_query(client: Client, query: str) -> QueryJob:
    query_job = client.query(query=query)
    return query_job


def format_results(query_job: QueryJob) -> List[Dict[str, Any]]:
    results = query_job.result()
    return [{key: value for key, value in row.items()} for row in results]



