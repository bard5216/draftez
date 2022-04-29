import logging
import requests
import sys
from app import app
from app.models import db
from app.models.conference import Conference
from app.models.division import Division
from app.models.team import Team
from app.models.player import Player


def getOr0(o, k):
    if k in o:
        return o[k]
    else:
        return 0


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


base_url = "https://statsapi.web.nhl.com/api/v1"

conferences_templ = base_url + "/conferences"
divisions_templ = base_url + "/divisions"
roster_templ = base_url + "/teams/{0}/roster"
player_templ = base_url + "/people/{0}"
player_stats_templ = base_url + "/people/{0}/stats?stats=statsSingleSeason"

if __name__ == '__main__':
    with app.app_context():
        r = requests.get(base_url + "/conferences")
        conferences = r.json()['conferences']
        for o in conferences:
            # print(f"{o['id']},{o['name']},{o['shortName']}\n")
            conf = Conference(id=o['id'], name=o['name'], shortname=o['shortName'])
            print("insert into conference(id, name, shortname) values ({0}, '{1}', '{2}');"
                  .format(o['id'], o['name'], o['shortName']))
            db.session.add(conf)
        db.session.commit()
