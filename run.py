import datetime
import json
import pathlib

from jinja2 import Template

from nhlsuomi.config import args, config
from nhlsuomi.logging import set_loglevel
from nhlsuomi.NHL import API, parser
from nhlsuomi.reddit import icydata

if __name__ == "__main__":
    set_loglevel(config.get('loglevel'))

    date = datetime.date.today() - datetime.timedelta(1)

    dumpfile = 'games-raw.json' if args.test_dump else ''
    games = API.fetch_games(date, dumpfile=dumpfile)
    icydata_submissions = icydata.fetch_submissions(**config.get('reddit'))

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
        config.get('nationalities', []),
        config.get('min_goals', 9),
        config.get('min_points', 9),
    )
    hilights, recaps = icydata.parse_hilights_recaps(
        icydata_submissions,
        config.get('hilights') + hilight_players,
        config.get('hilights_age_limit', 18)
    )

    schedule_config = config.get('schedule')
    if schedule_config:
        days = schedule_config['days']
        raw_schedule = API.fetch_upcoming_schedule(days)
        del schedule_config['days']
        schedule = list(parser.parse_schedule(raw_schedule, **schedule_config))
    else:
        schedule = []

    template_path = pathlib.Path(config.get('template'))
    template = Template(template_path.read_text())

    timestamp = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')

    html = template.render(
        results=results,
        hilights=hilights,
        recaps=recaps,
        timestamp=timestamp,
        schedule=schedule
    )

    output_path = pathlib.Path(config.get('output'))
    output_path.write_text(html)
