from logging import basicConfig, getLogger, Logger, FileHandler, StreamHandler, INFO
from datetime import date
from wb.config import LOGGER

basicConfig(
    level=INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=[
        FileHandler("{}/{}.log".format(LOGGER.get('PATH', '.'), date.today())),
        StreamHandler()
    ]
)


def get_logger(name: str) -> Logger:
    return getLogger(name)
