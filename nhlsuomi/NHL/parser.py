from itertools import chain
from operator import itemgetter
from typing import Iterable, List

from nhlsuomi.NHL.API import fetch_boxscore
from nhlsuomi.NHL.utils import pluck


def parse_games(obj: dict, timestamp: str) -> Iterable[dict]:
    total_games = obj.get('totalGames', 0)

    if total_games == 0:
        return []

    games = chain.from_iterable((
        date.get('games')
        for date
        in obj.get('dates', [])
        if date.get('date') == timestamp
    ))

    def status(game):
        state = pluck(game, 'status.abstractGameState')
        if state == 'Live':
            return 2
        elif state == 'Final':
            return 1
        else:
            return 0


    return [
        {
            'status': status(game),
            'id': game['gamePk'],
            'home': {
                'team': pluck(game, 'teams.home.team.abbreviation', '???'),
                'score': pluck(game, 'teams.home.score', 0)
            },
            'away': {
                'team': pluck(game, 'teams.away.team.abbreviation', '???'),
                'score': pluck(game, 'teams.away.score', 0)
            }
        }
        for game in games
        if 'gamePk' in game
    ]


def filter_players(players: dict,
                   nationalities: List[str],
                   min_goals: int,
                   min_points: int) -> Iterable[dict]:
    for player in players.values():
        goalie_toi = pluck(player, 'stats.goalieStats.timeOnIce', '0:00')

        if goalie_toi != '0:00':
            toi = goalie_toi
        else:
            toi = pluck(player, 'stats.skaterStats.timeOnIce', '0:00')

        if toi == '0:00':
            continue

        goals = pluck(player, 'stats.skaterStats.goals', 0)
        assists = pluck(player, 'stats.skaterStats.assists', 0)
        sv = round(pluck(player, 'stats.goalieStats.savePercentage', 0), 1)
        value = 2 + goals * 3 + assists

        if sv:
            shots = pluck(player, 'stats.goalieStats.shots', 0)
            value = (sv / 100)
        else:
            shots = pluck(player, 'stats.skaterStats.shots', 0)

        nationality = pluck(player, 'person.nationality', '?')
        if not ((goals + assists) >= min_points or goals >= min_goals):
            if nationality not in nationalities:
                continue

        yield {
            'first_name': pluck(player, 'person.firstName', '?'),
            'last_name': pluck(player, 'person.lastName', '?'),
            'nationality': nationality,
            'toi': toi,
            'shots': shots,
            'hits': pluck(player, 'stats.skaterStats.hits', 0),
            'plus_minus': pluck(player, 'stats.skaterStats.plusMinus', 0),
            'position': pluck(player, 'person.primaryPosition.abbreviation', '?'),
            'goals': goals,
            'assists': assists,
            'value': value,
            'sv': sv
        }


def parse_players(games: List[dict],
                  nationalities: List[str],
                  min_goals: int,
                  min_points: int) -> Iterable[dict]:

    def _extract(boxscore, team):
        return list(filter_players(
            pluck(boxscore, f'teams.{team}.players'),
            nationalities,
            min_goals,
            min_points
        ))

    result = []
    hilight_players = []

    for game in games:
        game_id = str(game.get('id'))
        boxscore = fetch_boxscore(game_id)
        home_players = _extract(boxscore, 'home')
        away_players = _extract(boxscore, 'away')
        players = sorted(
            (*home_players, *away_players),
            key=itemgetter('value'),
            reverse=True
        )
        status_value = game.get('status') * 1000
        value = sum((p.get('value', 0) for p in players)) + status_value

        hilight_players += list(filter(bool, (p['last_name'] for p in players)))

        game = {
            **game,
            **{
                'players': players,
                'value': value
            }
        }
        result.append(game)

    return (
        sorted(result, key=itemgetter('value'), reverse=True),
        list(set(hilight_players))
    )
