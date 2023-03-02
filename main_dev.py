import bigquery_utils
import config
import logger
import prepare_data

from main import query_data, publish_datastory


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

    logger.info("Publishing datastory...")
    publish_datastory(
        data=prepped_data,
        url=config.DATASTORY_DEV,
    )
    logger.info("Publishing datastory...Done")
