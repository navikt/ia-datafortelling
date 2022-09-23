import os

import pandas as pd
from google.cloud.bigquery import Client

import bigquery_utils
import config
import ds
import logger
import prepare_data


def query_data(client: Client, limit=None) -> [pd.DataFrame]:
    return bigquery_utils.query_dataframe(
        client=client,
        query=config.SQL_QUERY + ("" if limit is None else f" LIMIT {limit}")
    )


def publish_datastory(data: pd.DataFrame, url: str) -> None:
    _ds = ds.create_datastory(preppede_data=data)
    _ds.publish(url=url)


def update_datastory(data: {}, token: str, url: str) -> None:
    _ds = ds.create_datastory(preppede_data=data)
    _ds.update(token=token, url=url)


if __name__ == "__main__":
    logger = logger.get_logger()

    logger.info("Creating client...")
    bq_client = bigquery_utils.create_client()
    logger.info("Creating client...Done")

    logger.info("Querying data...")
    raw_data = query_data(client=bq_client, limit=None)
    logger.info("Querying data...Done")

    logger.info("Prepping data...")
    prepped_data = prepare_data.prep_data(raw_data)
    logger.info("Prepping data...Done")

    logger.info("Updating datastory...")
    update_datastory(
        data=prepped_data,
        url=config.DATASTORY_PROD,
        token=os.environ[config.TOKEN_SECRET_KEY],
    )
    logger.info("Updating datastory...Done")
