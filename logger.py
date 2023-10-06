import json
import logging


class KibanaFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        record.msg = json.dumps({"message": record.msg, "level": record.levelname})
        return super().format(record)


def get_logger(level=logging.INFO) -> logging.Logger:
    the_logger = logging.getLogger(name="ia-datafortelling")
    the_logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level=level)
    handler.setFormatter(KibanaFormatter())

    the_logger.handlers = [handler]

    return the_logger


log = get_logger()
