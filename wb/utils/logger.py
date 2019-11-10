from logging import basicConfig, getLogger, Logger, FileHandler, StreamHandler, INFO
from datetime import date
from config import LOGGER

HANDLERS = [StreamHandler()]

if (LOGGER.get('SAVE_TO_FILE', False)):
    HANDLERS.append(FileHandler("{}/{}.log".format(LOGGER.get('PATH', '.'), date.today())))

basicConfig(
    level=INFO,
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    handlers=HANDLERS
)


def get_logger(name: str) -> Logger:
    return getLogger(name)
