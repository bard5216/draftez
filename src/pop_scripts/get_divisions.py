import logging
import requests
from app import app
from app.models import db
from app.models.division import Division
from app.models.player import Player
from app.models.division import Division


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
        r = requests.get(divisions_templ)
        divisions = r.json()['divisions']
        for o in divisions:
            division = Division(id=o['id'], name=o['name'], shortname=o['abbreviation'])
            """
            division = Division(id=o['id'], name=o['name'], shortname=o['abbreviation'], conference_id=o['conference']['id'])
            print("insert into division(id, name, shortname, conference_id) values ({0}, '{1}', '{2}', {3});"
                  .format(o['id'], o['name'], o['abbreviation'], o['conference']['id']))
            """
            db.session.add(division)
        db.session.commit()
