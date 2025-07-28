import logging
import sys
import uuid

_request_id = str(uuid.uuid4())


def _setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        f"%(asctime)s | %(levelname)s | %(name)s | {_request_id} |\n%(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger


logger = _setup_logger()
