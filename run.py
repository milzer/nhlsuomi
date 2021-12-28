import argparse
import datetime
import json
import pathlib
from dataclasses import asdict

import yaml
from jinja2 import Template

from nhlsuomi.config import ConfigData
from nhlsuomi.logging import set_loglevel
from nhlsuomi.NHL import API, parser
from nhlsuomi.reddit import icydata


def parse_args():
    argparser = argparse.ArgumentParser()

    argparser.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        help='Config YML',
        required=True
    )

    argparser.add_argument(
        '--test-dump',
        help='Dump test data',
        action='store_true'
    )

    return argparser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    config = ConfigData(yaml.safe_load(args.config.read()))

    set_loglevel(config.loglevel)

    date = datetime.date.today() - datetime.timedelta(1)

    dumpfile = 'games-raw.json' if args.test_dump else ''
    games = API.fetch_games(date, dumpfile=dumpfile)

    icydata_submissions = icydata.fetch_submissions(
        config.reddit.client_id,
        config.reddit.client_secret
    )

    if args.test_dump:
        for data, filename in (
            (games, 'games.json'),
            (list(icydata_submissions), 'icydata.json')
        ):

            path = pathlib.Path.cwd() / 'tests' / filename
            print(f'Dumping {path}...', end='')
            path.write_text(json.dumps(data, indent=4))
            print('ok')

        exit(0)

    parsed_games = parser.parse_games(games, date)
    results, hilight_players = parser.parse_players(
        parsed_games,
        config.nationalities,
        config.min_goals,
        config.min_points
    )
    hilights, recaps = icydata.parse_hilights_recaps(
        icydata_submissions,
        config.hilight_keywords + hilight_players,
        config.hilights_age_limit
    )

    schedule_config = asdict(config.schedule)

    if schedule_config:
        days = schedule_config['days']
        raw_schedule = API.fetch_upcoming_schedule(days)
        del schedule_config['days']
        schedule = list(parser.parse_schedule(raw_schedule, **schedule_config))
    else:
        schedule = []

    template_path = pathlib.Path(config.template)
    template = Template(template_path.read_text())

    timestamp = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    html = template.render(
        results=results,
        hilights=hilights,
        recaps=recaps,
        timestamp=timestamp,
        schedule=schedule
    )

    output_path = pathlib.Path(config.output)
    output_path.write_text(html)
