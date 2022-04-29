import logging
import requests
from app import app
from app.models import db
from app.models.team import Team
from app.models.division import Division  # noqa: F401
from app.models.player import Player  # noqa: F401


def getOr0(o, k):
    if k in o:
        return o[k]
    else:
        return 0


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


base_url = "https://statsapi.web.nhl.com/api/v1"

roster_templ = base_url + "/teams/{0}/roster"
player_templ = base_url + "/people/{0}"
player_stats_templ = base_url + "/people/{0}/stats?stats=statsSingleSeason"

if __name__ == '__main__':
    with app.app_context():
        r = requests.get(base_url + "/teams")
        teams = r.json()['teams']
        for o in teams:
            print("insert into team(id, name, shortname, abbrev, division_id) values ({0}, '{1}', '{2}', '{3}', {4});"
                  .format(o['id'], o['name'], o['teamName'], o['abbreviation'], o['division']['id']))

            team = Team(id=o['id'], name=o['name'], shortname=o['teamName'], abbrev=o['abbreviation'], division_id=o['division']['id'])
            db.session.add(team)

        db.session.commit()
