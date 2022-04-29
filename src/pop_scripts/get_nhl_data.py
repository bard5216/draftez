
import requests
from dotenv import load_dotenv
from app.models import db
from app.models.conference import Conference
from app.models.division import Division


base_url = "https://statsapi.web.nhl.com/api/v1/"


def build_url(path):
    return base_url + path


def get_nhl_list(list_type):
    """ conferences, divisions, teams
    """
    r = requests.get(build_url(list_type))
    # print(f"status code from get {list_type}={r.status_code}\n")
    json = r.json()
    return json


def get_nhl_team_roster(team_id):
    r = requests.get(build_url(f"teams/{team_id}/roster"))
    return r.json()


def get_nhl_player_stats(player_id):
    r = requests.get(build_url(f"people/{player_id}/stats?stats=statsSingleSeason")
    return r.json()


if __name__ == '__main__':
    resp = get_nhl_list('conferences')
    for o in resp['conferences']:
        # print(f"{o['id']},{o['name']},{o['shortName']}\n")
        # conf = Conference(id=o['id'], name=o['name'], shortname=o['shortName'])
        print("insert into conference(id, name, shortname) values ({0}, '{1}', '{2}');\n"
              .format(o['id'], o['name'], o['shortName']))
        # conf = Conference(name=o['name'], shortname=o['shortName'])
        # db.session.add(conf)

    resp = get_nhl_list('divisions')
    for o in resp['divisions']:
        print("insert into division(id, name, shortname, conference_id) values ({0}, '{1}', '{2}', {3});\n"
              .format(o['id'], o['name'], o['nameShort'], o['conference']['id']))

    resp = get_nhl_list('teams')
    for t in resp['teams']:
        print("insert into team(id, name, shortname, abbrev, division_id) values ({0}, '{1}', '{2}', '{3}', {4});\n"
              .format(t['id'], t['name'], t['teamName'], t['abbreviation'], t['division']['id']))
        team_resp = get_nhl_team_roster(t['id'])
        for p in team_resp['roster']:
            pers = p['person']
            pos = p['position']
            print("insert into player (id, full_name, team_id, position) values ({0}, '{1}', {2}, '{3}');\n"
                  .format(pers['id'], pers['fullName'], t['id'], pos['type']))
