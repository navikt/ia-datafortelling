import os

import pandas as pd
from google.cloud.bigquery import Client

import bigquery_utils
import config
import ds
import logging
import prepare_data


def query_data(client: Client, limit=None) -> [pd.DataFrame]:
    return bigquery_utils.query_dataframe(
        client=client,
        query=config.SQL_QUERY + ("" if limit is None else f" LIMIT {limit}"),
    )


def publish_datastory(data: pd.DataFrame, url: str) -> None:
    _ds = ds.create_datastory(preppede_data=data)
    _ds.publish(url=url)


def update_datastory(data: {}, token: str, url: str) -> None:
    _ds = ds.create_datastory(preppede_data=data)
    _ds.update(token=token, url=url)


def load_and_publish():
    logger = logging.get_logger()

    logger.info("Prepping data...")
    prepped_data = prepare_data.prep_data(raw_data)
    logger.info("Prepping data...Done")

    logger.info("Updating datastory...")

    # TODO: do quarto-stuff instead
    # update_datastory(
    #     data=prepped_data,
    #     url=config.DATASTORY_PROD,
    #     token=os.environ[config.TOKEN_SECRET_KEY],
    # )
    logger.info("Updating datastory...Done")


if __name__ == "__main__":
    load_and_publish()
