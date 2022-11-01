from datetime import date

from nhlsuomi import VERSION
from nhlsuomi.logging import logger
from nhlsuomi.NHL import API, parser

if __name__ == '__main__':
    logger.setLevel(10)
    logger.info(f'NHLSuomi v{VERSION}')

    schedule = API.get_schedule(date(2022, 10, 19))

    for game in parser.parse_schedule_games(schedule):
        print(game)
