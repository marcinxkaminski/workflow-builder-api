from logging import basicConfig, getLogger, Logger, FileHandler, StreamHandler, INFO
from datetime import date
from wb.config import LOGGER
from os import path

HANDLERS = [StreamHandler()]

if LOGGER.get("SAVE_TO_FILE", False):
    filepath = path.join(LOGGER.get("PATH", "."), f"{date.today()}.log")
    file_handler = None
    try:
        file_handler = FileHandler(filepath)
    except FileNotFoundError:
        with open(filepath, "w"):
            file_handler = FileHandler(filepath)

    HANDLERS.append(file_handler)

basicConfig(
    level=INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=HANDLERS,
)


def get_logger(name: str) -> Logger:
    return getLogger(name)
