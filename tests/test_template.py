import unittest
from textwrap import dedent

from nhlsuomi import html
from nhlsuomi.data import Game, Goalie, Skater


class TestParser(unittest.TestCase):
    def test_template(self):
        template = dedent(
            """
            <html>
            <body>

            {{timestamp}}

            {% for skater in highlight_skaters %}
                {{skater.first_name}} {{skater.last_name}} {{skater.g}}+{{skater.a}}
            {% endfor %}

            {% for game in games %}
                {{game.home_team}} {{game.home_score}} - {{game.away_score}} {{game.away_team}}
                {% for skater in game.skaters %}
                    {{skater.columns}}
                {% endfor %}
                {% for goalie in game.goalies %}
                    {{goalie.columns}}
                {% endfor %}
            {% endfor %}

            {% for datetime, home, away in schedule %}
                {{datetime}} - {{away}}@{{home}}
            {% endfor %}

            </body>
            </html>
        """
        )

        expected = dedent(
            """
            <html>
            <body>
            1.12.2022 12:34:56
            A B 5+1
            C D 1+4
            ARI 1 - 2 COL
            ('E', 'F', '1+0', '05:00', 0, 0, 0, 0)
            ('A', 'B', '0+1', '01:40', 1, 1, 1, 2)
            ('C', 'D', '0+0', '03:20', 1, 1, 1, 2)
            ('I', 'J', '92.6%', '60:00', 20)
            ('G', 'H', '81.1%', '40:00', 10)
            BOS 2 - 1 BUF
            2.12. 21:00 - away1@home1
            3.13. 22:00 - away2@home2
            </body>
            </html>
        """
        ).strip()

        games = sorted(
            [
                Game('BOS', 2, 'BUF', 1, True, 1, 'https://recap/1'),
                Game(
                    'ARI',
                    1,
                    'COL',
                    2,
                    True,
                    1,
                    'https://recap/2',
                    sorted(
                        [
                            Skater('A', 'B', 0, 1, 100, 1, 1, 1, 2, 'FIN'),
                            Skater('C', 'D', 0, 0, 200, 1, 1, 1, 2, 'FIN'),
                            Skater('E', 'F', 1, 0, 300, 0, 0, 0, 0, 'FIN'),
                        ]
                    ),
                    sorted(
                        [
                            Goalie('G', 'H', 0.81123, 40 * 60, 10, 'FIN'),
                            Goalie('I', 'J', 0.92567, 60 * 60, 20, 'FIN'),
                        ]
                    ),
                ),
            ]
        )

        skater_highlights = [
            Skater('A', 'B', 5, 1, 1, 1, 1, 1, 1, 'CAN'),
            Skater('C', 'D', 1, 4, 1, 1, 1, 1, 1, 'SWE'),
        ]

        schedule = [
            ('2.12. 21:00', 'home1', 'away1'),
            ('3.13. 22:00', 'home2', 'away2'),
        ]

        result = html.render(
            template,
            games,
            skater_highlights,
            schedule,
            '1.12.2022 12:34:56',
        )

        self.assertEqual(result, expected)
