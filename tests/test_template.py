import unittest
from textwrap import dedent

from nhlsuomi import html
from nhlsuomi.data import Game, Goalie, Skater


class TestParser(unittest.TestCase):
    def test_template(self):
        template = dedent('''
            <html>
            <body>

            {{timestamp}}

            {% for title, url in highlights %}
                {{title}} {{url}}
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

            {% for datetime, game in schedule %}
                {{datetime}} - {{game}}
            {% endfor %}

            </body>
            </html>
        ''')

        expected = dedent('''
            <html>
            <body>
            1.12.2022 12:34:56
            title1 https://highlight/1
            title2 https://highlight/2
            ARI 1 - 2 COL
            ('E', 'F', '1+0', '05:00', 0, 0, 0, 0)
            ('A', 'B', '0+1', '01:40', 1, 1, 1, 2)
            ('C', 'D', '0+0', '03:20', 1, 1, 1, 2)
            ('I', 'J', '92.6%', '60:00', 20)
            ('G', 'H', '81.1%', '40:00', 10)
            BOS 2 - 1 BUF
            2.12. 21:00 - game
            3.13. 22:00 - other game
            </body>
            </html>
        ''').strip()

        games = sorted([
            Game('BOS', 2, 'BUF', 1, True, 1, 'https://recap/1'),
            Game(
                'ARI', 1, 'COL', 2, True, 1, 'https://recap/2',
                sorted([
                    Skater('A', 'B', 0, 1, 100, 1, 1, 1, 2),
                    Skater('C', 'D', 0, 0, 200, 1, 1, 1, 2),
                    Skater('E', 'F', 1, 0, 300, 0, 0, 0, 0)
                ], reverse=True),
                sorted([
                    Goalie('G', 'H', 0.81123, 40 * 60, 10),
                    Goalie('I', 'J', 0.92567, 60 * 60, 20)
                ], reverse=True)
            ),
        ], reverse=True)

        highlights = [
            ('title1', 'https://highlight/1'),
            ('title2', 'https://highlight/2'),
        ]

        schedule = [
            ('2.12. 21:00', 'game'),
            ('3.13. 22:00', 'other game')
        ]

        result = html.render(template, games, highlights, schedule, '1.12.2022 12:34:56')

        self.assertEqual(result, expected)
