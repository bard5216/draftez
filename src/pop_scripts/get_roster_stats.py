import logging
import requests
import sys
from app import app
from app.models import db
from app.models.team import Team
from app.models.player import Player
from app.models.division import Division  # noqa: F401


def getOr0(o, k):
    if k in o:
        return o[k]
    else:
        return 0


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


base_url = "https://statsapi.web.nhl.com/api/v1"

roster_templ = base_url + "/teams/{0}/roster"
people_stats_templ = base_url + "/people/{0}/stats?stats=statsSingleSeason"


if __name__ == '__main__':
    argc = len(sys.argv)
    # print(f"argc={argc}")
    if argc != 2:
        print(f"Usage: {sys.argv[0]} <team_id>")
        # print("       season: 20192020\n")
        sys.exit(1)

    team_id = sys.argv[1]
    # season = sys.argv[2]

    with app.app_context():
        team = Team.query.filter(Team.id == team_id).one()
        # print(f"team name is {team.name}")

        players = Player.query.filter(Player.team_id == team_id)

        for player in players:
            try:
                r = requests.get(people_stats_templ.format(player.id))
                if r.status_code == 200:
                    obj = r.json()
                    season = obj['stats'][0]['splits'][0]
                    # stat = obj['stats'][0]['splits'][0]['stat']
                    stat = season['stat']
                    player.season = season['season']
                    player.games = stat.get('games')
                    player.goals = stat.get('goals')
                    player.assists = stat.get('assists')
                    player.points = stat.get('points')
                    db.session.commit()
            except Exception as e:  # NO
                print(f"Error {e} accessing player stats for player {player.id} on team {team.id}")

        """
        for rost_obj in roster_list:
            pers = rost_obj['person']
            pos = rost_obj['position']
            # print("{0},{1}".format(person['id'], person['fullName']));

            r = requests.get(player_templ.format(pers['id']))
            pers_detail = r.json()['people'][0]

            r = requests.get(player_stats_templ.format(pers['id']))
            stats = r.json()['stats'][0]['splits'][0]
            stat = stats['stat']

            print("insert "
                "into player (id, full_name, first_name, last_name, team_id, position, season, goals, assists, points) "
                "values ({0}, '{1}', '{2}', '{3}', {4}, '{5}', '{6}', {7}, {8}, {9});"
                .format(pers['id'], pers['fullName'], pers_detail['firstName'],
                        pers_detail['lastName'], team_id, pos['type'][0],
                        stats['season'], getOr0(stat, 'goals'),
                        getOr0(stat, 'assists'), getOr0(stat, 'points')))
        """
