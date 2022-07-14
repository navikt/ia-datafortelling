import json
import logging


class KibanaFormatter(logging.Formatter):
    def __init__(self):
        super().__init__()

    def format(self, record):
        record.msg = json.dumps({"message": record.msg, "level": record.levelname})
        return super().format(record)


def get_logger(level=logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name="ia-datafortelling")
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setLevel(level=level)
    handler.setFormatter(KibanaFormatter())

    logger.handlers = [handler]

    return logger
