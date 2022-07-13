import json
from typing import List, Sequence, Dict, Any

import pandas as pd
from google.cloud.bigquery import Client, DatasetReference, TableReference
from google.cloud.bigquery.job import QueryJob


def create_client() -> Client:
    # secrets_file = "secrets.json"
    # envs = None
    # with open(secrets_file) as file:
    #     envs = json.loads(file.read())

    client = Client(project="teamia-prod-df3d")
    return client


def create_table_ref(project_id: str, dataset_id: str,
      table_id: str) -> TableReference:
    dataset_ref = DatasetReference(project=project_id, dataset_id=dataset_id)
    table_ref = dataset_ref.table(table_id=table_id)
    return table_ref


def write_to_table(client: Client, table: TableReference, rows: List[Dict]) -> \
Sequence[Dict]:
    errors = client.insert_rows_json(table=table, json_rows=rows)
    return errors


def execute_query(client: Client, query: str) -> QueryJob:
    query_job = client.query(query=query)
    return query_job


def format_results(query_job: QueryJob) -> List[Dict[str, Any]]:
    results = query_job.result()
    return [{key: value for key, value in row.items()} for row in results]


def query_dataframe(client: Client, query: str) -> pd.DataFrame:
    query_job = execute_query(client=client, query=query)
    return pd.DataFrame(data=format_results(query_job=query_job))
