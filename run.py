import argparse
import dataclasses
import json
import pathlib
import time
from datetime import datetime, timedelta
from itertools import chain
from typing import List, Union

from nhlsuomi import VERSION
from nhlsuomi.config import Config
from nhlsuomi.data import Skater
from nhlsuomi.html import render
from nhlsuomi.logging import logger
from nhlsuomi.nhl import api, parser


def loglevel(value: str) -> Union[int,str]:
    try:
        return int(value)
    except ValueError:
        return value.upper()


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('config', type=pathlib.Path, help='Config file')
    argparser.add_argument('--loglevel', type=loglevel, default='INFO')
    args = argparser.parse_args()

    logger.setLevel(args.loglevel)
    logger.info(f'NHLSuomi v{VERSION}')

    config = Config.load(args.config)

    games_date = datetime.today().date() + timedelta(config.date_offset)

    if config.schedule_days:
        schedule_date = games_date + timedelta(1)
        upcoming_schedule = api.get_schedule(schedule_date, config.schedule_days)
        upcoming_games = list(parser.parse_schedule_upcoming(
            upcoming_schedule,
            config.schedule_timezone,
            config.schedule_hours_from,
            config.schedule_hours_to,
            config.schedule_datetime_format
        ))
    else:
        upcoming_games = []

    start_time = time.time()

    while True:
        schedule = api.get_schedule(games_date)
        games = list(parser.parse_schedule_games(schedule))

        ongoing_games = [game.final for game in games].count(False)

        highlight_skaters: List[Skater] = []

        for game in games:
            if not game.final:
                continue

            def filter_and_sort_players(players: List) -> List:
                return sorted((
                    player for player in players
                    if not config.nationalities or player.nationality in config.nationalities
                ))

            boxscore = api.get_boxscore(game.gamecenter_id)
            skaters, goalies = parser.parse_boxscore_players(boxscore)
            game.skaters = filter_and_sort_players(skaters)
            game.goalies = filter_and_sort_players(goalies)

            highlight_skaters.extend(
                skater
                for skater in skaters
                if (
                    skater.nationality not in config.nationalities
                    and (
                        skater.g >= config.highlight_skater_g
                        or (skater.g + skater.a) >= config.highlight_skater_p
                    )
                )
            )

        games = sorted(games)

        highlight_keywords = set(chain.from_iterable(game.last_names for game in games))
        highlights = list(parser.parse_schedule_highlights(schedule, highlight_keywords))

        template = pathlib.Path(config.template).read_text()
        html = render(template, games, highlights, sorted(highlight_skaters), upcoming_games)

        pathlib.Path(config.output).write_text(html)

        if not ongoing_games:
            break

        run_time_s = int(time.time() - start_time)
        if run_time_s >= config.quit_minutes * 60:
            logger.info(f'Quitting with {ongoing_games} ongoing games')
            break

        logger.debug(f'Waiting for {ongoing_games} games...')
        time.sleep(config.refresh_minutes * 60)

    if config.jsondump:
        dumpfile = pathlib.Path(config.jsondump)
        logger.info(f'Dump JSON to {dumpfile.resolve()}')
        json_text = json.dumps({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'games': [dataclasses.asdict(game) for game in games],
            'highlights': highlights,
            'schedule': upcoming_games
        })
        dumpfile.write_text(json_text)
