import logging
import requests
import sys
from app import app
from app.models import db
from app.models.player import Player
from app.models.team import Team  # noqa: F401
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
people_templ = base_url + "/people/{0}"


if __name__ == '__main__':
    argc = len(sys.argv)
    # print(f"argc={argc}")
    if argc != 2:
        print(f"Usage: {sys.argv[0]} <team_id>\n")
        sys.exit(1)

    team_id = sys.argv[1]
    r = requests.get(roster_templ.format(team_id))
    roster_list = r.json()['roster']

    with app.app_context():

        for rost_obj in roster_list:
            pers = rost_obj['person']
            pos = rost_obj['position']
            # print("{0},{1}".format(person['id'], person['fullName']));

            """
            r = requests.get(player_templ.format(pers['id']))
            pers_detail = r.json()['people'][0]

            r = requests.get(player_stats_templ.format(pers['id']))
            stats = r.json()['stats'][0]['splits'][0]
            stat = stats['stat']
            """

            print("insert into player (id, full_name, team_id, position) "
                  "values ({0}, '{1}', '{2}', '{3}');"
                  .format(pers['id'], pers['fullName'], team_id, pos['type'][0]))

            player = Player(id=pers['id'], full_name=pers['fullName'], team_id=team_id, position=pos['type'][0])

            try:
                r = requests.get(people_templ.format(player.id))
                if r.status_code == 200:
                    obj = r.json()
                    if 'people' in obj:
                        person_detail = obj['people'][0]
                        player.first_name = person_detail['firstName']
                        player.last_name = person_detail['lastName']
            except Exception as e:  # NO
                print(f"Error {e} accessing player detail for player {player.id}")

            db.session.commit()


            db.session.add(player)

        db.session.commit()
