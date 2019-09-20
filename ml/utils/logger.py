import logging

logging.basicConfig(
    filename='app.log', level=logging.INFO, format='%(asctime)s | %(levelname)s | %(name)s | %(message)s'
)


def get_logger(name: str = __name__):
    return logging.getLogger(name)
