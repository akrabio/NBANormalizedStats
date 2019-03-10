from nba_py import team
from nba_py import constants
import json


class Team:
    def __init__(self, team_id, from_year=None, to_year=None):
        self.team_id = team_id
        self.team_stats = get_team_averages(team_id)


def get_team_averages(team_id):
    return team.TeamSeasons(team_id=team_id, season_type='Regular Season', per_mode=constants.PerMode.PerGame).json[
        'resultSets'][0]['rowSet']


if __name__ == '__main__':
    jazz = Team(constants.TEAMS['UTA']['id'])
    print json.dumps(jazz.team_stats, indent=4)
