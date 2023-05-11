import logging
from logging.handlers import RotatingFileHandler

from tracker.settings import BASE_DIR, DT_FORMAT, ENCODING, LOG_FORMAT


def configure_logging() -> None:
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'parser.log'
    rotating_handler = RotatingFileHandler(log_file, maxBytes=10**6,
                                           encoding=ENCODING, backupCount=5)
    logging.basicConfig(
        datefmt=DT_FORMAT, format=LOG_FORMAT, level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
