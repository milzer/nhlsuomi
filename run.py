import argparse
import datetime
import json
import pathlib

from jinja2 import Template

from nhlsuomi.NHL import API, parser
from nhlsuomi.reddit import icydata

argparser = argparse.ArgumentParser()
argparser.add_argument('-c', '--config', type=argparse.FileType('r'),
                       help='Config JSON', required=True)
argparser.add_argument('--test-dump', help='Dump test data', action='store_true')
args = argparser.parse_args()

DEFAULT_TZOFFSET = 6

if __name__ == "__main__":
    config = json.loads(args.config.read())

    date = (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')

    games = API.fetch_games(date)
    icydata_submissions = icydata.fetch_submissions(**config.get('reddit'))

    if args.test_dump:
        for data, filename in ((games, 'games.json'),
                               (list(icydata_submissions), 'icydata.json')):

            path = pathlib.Path.cwd() / 'tests' / filename
            print(f'Dumping {path}...', end='')
            path.write_text(json.dumps(data, indent=4))
            print('ok')

        exit(0)

    parsed_games = parser.parse_games(games, date)
    results = parser.parse_players(parsed_games, config.get('nationalities'))
    hilights, recaps = icydata.parse_hilights_recaps(
        icydata_submissions,
        config.get('hilights'),
        config.get('tzoffset', DEFAULT_TZOFFSET)
    )

    template_path = pathlib.Path(config.get('template'))
    template = Template(template_path.read_text())

    timestamp = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    html = template.render(
        results=results,
        hilights=hilights,
        recaps=recaps,
        timestamp=timestamp
    )

    output_path = pathlib.Path(config.get('output'))
    output_path.write_text(html)
