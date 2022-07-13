import logging
import os
from typing import Sequence

import pandas as pd
from google.cloud.bigquery import Client

import bq_utils
import config
import ds
import dtos
import fetch_metrics


def get_logger() -> logging.Logger:
    _logger = logging.getLogger(name="Brukernotifkasjoner datastory")
    _logger.setLevel(level=logging.INFO)

    handler = logging.StreamHandler()
    handler.setLevel(level=logging.INFO)

    _logger.handlers = [handler]

    return _logger


def load_metrics(bq_client: Client, url: str, token: str) -> Sequence:
    raw_metrics = fetch_metrics.fetch_brukernotifkasjoner_metrics(url=url,
                                                                  token=token)
    metrics = [dtos.BrukerNotifikasjonerMetric.from_dict(row).prep() for row in
               raw_metrics]

    table = bq_utils.create_table_ref(project_id=config.PROJECT,
                                      dataset_id=config.DATASET,
                                      table_id=config.TABLE)
    errors = bq_utils.write_to_table(client=bq_client, table=table,
                                     rows=metrics)

    return errors


def fetch_data(bq_client: Client) -> [pd.DataFrame]:
    query_job = bq_utils.execute_query(client=bq_client, query=config.SQL_QUERY)
    raw_data = bq_utils.format_results(query_job=query_job)

    df = pd.DataFrame(raw_data)
    df['opprettet_year'] = df['opprettet'].dt.year
    df['opprettet_month'] = df['opprettet'].dt.month

    unike_måned = df.groupby(["opprettet_year", "opprettet_month"]).nunique()
    unike_år = df.groupby("opprettet_year").nunique()

    return [unike_måned, unike_år]


def publish_datastory(data: pd.DataFrame, url: str) -> None:
    _ds = ds.create_datastory(data=data)
    _ds.publish(url=url)


def update_datastory(data: pd.DataFrame, token: str, url: str) -> None:
    _ds = ds.create_datastory(data=data)
    _ds.update(token=token, url=url)


if __name__ == "__main__":
    logger = get_logger()

    logger.info("Creating client....")
    client = bq_utils.create_client()
    logger.info("Creating client....Done")

    logger.info("Fetching data....")
    prepped_data = fetch_data(bq_client=client)
    logger.info("Fetching data....Done")

    logger.info("Updating datastory....")
    update_datastory(
        data=prepped_data[1],
        url=config.DATASTORY_PROD,
        token=os.environ["DATASTORY_TOKEN"])
    logger.info("Updating datastory....Done")
