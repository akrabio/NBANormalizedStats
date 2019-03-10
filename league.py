import team
import consts

from nba_py import constants
from numpy import mean

name_to_index = {consts.points: 32, consts.assists: 27, consts.rebounds: 26, consts.steals: 29, consts.blocks: 31,
                 'year': 3}


class League:
    def __init__(self):
        self.teams = get_teams_info()

    def calculate_league_average(self, from_year, to_year):
        points = []
        rebounds = []
        steals = []
        blocks = []
        assists = []
        for team_object in self.teams:
            point_av = get_average(consts.points, team_object.team_stats, from_year, to_year)
            if point_av > 0:
                points.append(point_av)
            rebound_av = get_average(consts.rebounds, team_object.team_stats, from_year, to_year)
            if rebound_av > 0:
                rebounds.append(rebound_av)
            steal_av = get_average(consts.steals, team_object.team_stats, from_year, to_year)
            if steal_av > 0:
                steals.append(steal_av)
            block_av = get_average(consts.blocks, team_object.team_stats, from_year, to_year)
            if block_av > 0:
                blocks.append(block_av)
            assist_av = get_average(consts.assists, team_object.team_stats, from_year, to_year)
            if assist_av > 0:
                assists.append(assist_av)

        if not points:
            return None
        return {
            consts.points: mean(points),
            consts.rebounds: mean(rebounds),
            consts.steals: mean(steals),
            consts.blocks: mean(blocks),
            consts.assists: mean(assists)
        }


def get_teams_info():
    teams = []
    for team_name, team_info in constants.TEAMS.iteritems():
        team_object = team.Team(team_info['id'])
        # if team_object.team_stats['points'] <= 0:
        #     continue
        teams.append(team_object)
    return teams


def get_average(category, stats, from_year, to_year):
    if int(from_year[:-3]) < 1960:
        from_year = '1960-61'
    if int(from_year[:-3]) > 2017:
        from_year = '2017-18'
    if int(to_year[:-3]) > 2017:
        to_year = '2017-18'
    if int(to_year[:-3]) < 1960:
        to_year = '1960-61'

    averages = []
    for year in stats:
        a = int(from_year[:-3])
        b = int(year[name_to_index['year']][:-3])
        c = int(to_year[:-3])
        if a <= b <= c:
            value = year[name_to_index[category]]
            if value <= 0:
                continue
            averages.append(value)
        if b > c:
            break
    if not averages:
        return 0
    return mean(averages)


if __name__ == '__main__':
    league = League()
