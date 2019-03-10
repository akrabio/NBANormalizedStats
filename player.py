from nba_py import player
from numpy import mean

import league
from consts import all_time_stats
import consts

name_to_index = {'season': 1, consts.rebounds: 20, consts.assists: 21, consts.steals: 22, consts.blocks: 23, consts.points: 26}


class Player:
    def __init__(self, first, last):
        print 'Getting {} {}\'s info'.format(first, last)
        try:
            player_info = player.get_player(first_name=first, last_name=last, just_id=False)
        except player.PlayerNotFoundException:
            print 'Could not find player'
            exit()
        else:
            print 'Got {} {}\'s info'.format(first, last)
            player_id = player_info.iloc[0]['PERSON_ID']
            print 'Getting player stats'
            player_object = player.PlayerCareer(player_id=player_id)
            self.career_stats = get_career_stats(player_object.regular_season_career_totals())
            player_stats = player_object.json['resultSets'][0]['rowSet']
            print 'Got player stats'
            seasons = {}
            for season_object in player_stats:
                seasons[season_object[name_to_index['season']]] = {consts.points: season_object[name_to_index[consts.points]],
                                                                   consts.rebounds: season_object[name_to_index[consts.rebounds]],
                                                                   consts.assists: season_object[name_to_index[consts.assists]],
                                                                   consts.steals: season_object[name_to_index[consts.steals]],
                                                                   consts.blocks: season_object[name_to_index[consts.blocks]]}
            normalized_seasons = []
            print 'Getting team stats'
            league_object = league.League()
            for season, stats in sorted(seasons.iteritems()):
                print 'Getting stats for season {}'.format(season)
                season_stats = league_object.calculate_league_average(from_year=season, to_year=season)
                normalized_seasons.append(normalize_season(self, season_stats, stats))
            self.normalized_career_stats = get_career_average(normalized_seasons)


def normalize_season(player, season_stats, player_stats):
    if season_stats is None:
        season_stats = consts.all_time_stats
    normalized_stats = {}
    for category in all_time_stats:
        player_stats[category] = player.career_stats[category] if player_stats[category] is None else player_stats[category]
        normalized_stats[category] = (all_time_stats[category] / season_stats[category]) * player_stats[category]
    return normalized_stats


def get_career_stats(player_stats):
    return {
            consts.points: player_stats.iloc[0][consts.points],
            consts.rebounds: player_stats.iloc[0][consts.rebounds],
            consts.assists: player_stats.iloc[0][consts.assists],
            consts.steals: player_stats.iloc[0][consts.steals],
            consts.blocks: player_stats.iloc[0][consts.blocks],
            }


def get_career_average(seasons_average):
    points = []
    rebounds = []
    steals = []
    blocks = []
    assists = []
    for season in seasons_average:
        points.append(season[consts.points])
        rebounds.append(season[consts.rebounds])
        assists.append(season[consts.assists])
        steals.append(season[consts.steals])
        blocks.append(season[consts.blocks])
    return {
            consts.points: mean(points),
            consts.rebounds: mean(rebounds),
            consts.assists: mean(assists),
            consts.steals: mean(steals),
            consts.blocks: mean(blocks)
        }


if __name__ == '__main__':

    # player = Player('michael', 'jordan')
    player = Player('patrick', 'ewing')
    print 'Career stats: {}'.format(player.career_stats)
    print 'Normalized career stats: {}'.format(player.normalized_career_stats)
    # print player.player_stats
