import argparse

import yaml

_defaults = {
    'loglevel': 'INFO',
    'reddit': {
        'username': '',
        'password': '',
        'client_id': '',
        'client_secret': ''
    },
    'nationalities': [
        'FIN'
    ],
    'min_goals': 3,
    'min_points': 5,
    'template': 'template.html',
    'output': 'nhl.html',
    'hilights_age_limit': 18,
    'hilight_keywords': [],
    'schedule': {
        'days': 7,
        'timezone': 'Europe/Helsinki',
        'dt_format': '%-d.%-m. %H:%M',
        'hours': [
            0,
            24
        ]
    }
}

_argparser = argparse.ArgumentParser()
_argparser.add_argument(
    '-c',
    '--config',
    type=argparse.FileType('r'),
    help='Config YML',
    required=True
)
_argparser.add_argument(
    '--test-dump',
    help='Dump test data',
    action='store_true'
)

args = _argparser.parse_args()

config = {
    **_defaults,
    **yaml.safe_load(args.config.read())
}
