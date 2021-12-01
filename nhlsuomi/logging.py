import logging
import sys
from typing import Optional, Union

logger = logging.getLogger('nhlsuomi')
logger.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

logger.addHandler(ch)


def set_loglevel(level: Optional[Union[int,str]]):
    if level is None:
        return
    elif str(level).isdigit():
        int_level = int(level)
    else:
        try:
            int_level = int(getattr(logging, str(level)))
        except Exception:
            logger.warning(f'Ignoring invalid loglevel: {level}')
            return

    logger.info(f'Setting loglevel: {int_level}')
    logger.setLevel(int_level)
    ch.setLevel(int_level)


def _excepthook(exc_type, exc_value, exc_traceback):
    if not issubclass(exc_type, Exception):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = _excepthook
