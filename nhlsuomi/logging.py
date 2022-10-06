import logging
import sys


class Formatter(logging.Formatter):
    def __init__(self):
        super().__init__('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def format(self, record: logging.LogRecord) -> str:
        if record.exc_info:
            record.levelname = 'EXCEPTION'

        return super().format(record)


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(Formatter())

logger = logging.getLogger('nhlsuomi')
logger.addHandler(handler)


def _excepthook(exc_type, exc_value, exc_traceback = None):
    if issubclass(exc_type, Exception):
        logger.error('Uncaught exception', exc_info=(exc_type, exc_value, exc_traceback))
    else:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)


sys.excepthook = _excepthook
