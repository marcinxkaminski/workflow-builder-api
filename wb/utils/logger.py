from logging import basicConfig, getLogger, Logger, FileHandler, StreamHandler, INFO
from datetime import date
from config import LOGGER
from os import path

HANDLERS = [StreamHandler()]

if LOGGER.get("SAVE_TO_FILE", False):
    filename = f"{date.today()}.log"
    HANDLERS.append(FileHandler(path.join(LOGGER.get("PATH", "."), filename)))

basicConfig(
    level=INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=HANDLERS,
)


def get_logger(name: str) -> Logger:
    return getLogger(name)
