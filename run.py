from nhlsuomi import VERSION
from nhlsuomi.logging import logger

if __name__ == '__main__':
    logger.setLevel(10)
    logger.info(f'NHLSuomi v{VERSION}')
