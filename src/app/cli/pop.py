import click
import logging
import requests
# import pprint
from flask import Blueprint

from app.models import (
    db,
    Conference,
    Division,
    Team,
    Player,
)


bp = Blueprint("cli_pop", __name__)
logger = logging.getLogger(__name__)


@bp.cli.command("full")
def populate_all():
    get_conferences()
    get_divisions()
    get_teams()


logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


base_url = "https://statsapi.web.nhl.com/api/v1"

conferences_templ = base_url + "/conferences"
divisions_templ = base_url + "/divisions"
roster_templ = base_url + "/teams/{0}/roster"
player_templ = base_url + "/people/{0}"
player_stats_templ = base_url + "/people/{0}/stats?stats=statsSingleSeason"


@bp.cli.command("conferences")
def get_conferences():
    r = requests.get(base_url + "/conferences")
    conferences = r.json()['conferences']
    for o in conferences:
        # print(f"{o['id']},{o['name']},{o['shortName']}\n")
        conf = Conference(id=o['id'], name=o['name'], shortname=o['shortName'])
        print(
            "insert into conference(id, name, shortname) values ({0}, '{1}', '{2}');"
            .format(o['id'], o['name'], o['shortName'])
        )
        db.session.add(conf)
    db.session.commit()


@bp.cli.command("divisions")
def get_divisions():
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


@bp.cli.command("teams")
def get_teams():
    r = requests.get(base_url + "/teams")
    teams = r.json()['teams']
    for o in teams:
        # print("insert into team(id, name, shortname, abbrev, division_id) values ({0}, '{1}', '{2}', '{3}', {4});"
        #        .format(o['id'], o['name'], o['teamName'], o['abbreviation'], o['division']['id']))

        print(f"Adding team {o['teamName']}")
        team = Team(id=o['id'], name=o['name'], shortname=o['teamName'], abbrev=o['abbreviation'], division_id=o['division']['id'])
        db.session.add(team)
        db.session.commit()
        get_team_roster(team.id)


def get_team_roster(team_id):
    r = requests.get(roster_templ.format(team_id))
    roster_list = r.json()['roster']

    for rost_obj in roster_list:
        pers = rost_obj['person']
        pos = rost_obj['position']
        player = Player(id=pers['id'], full_name=pers['fullName'], team_id=team_id, position=pos['type'][0])

        try:
            r = requests.get(player_templ.format(player.id))
            if r.status_code == 200:
                obj = r.json()
                if 'people' in obj:
                    person_detail = obj['people'][0]
                    player.first_name = person_detail['firstName']
                    player.last_name = person_detail['lastName']
        except Exception as e:  # NO
            print(f"Error {e} accessing player detail for player {player.id}")

        db.session.add(player)

    db.session.commit()


@bp.cli.command("stats")
def get_team_roster_stats():
    teams = db.session.query(Team).all()
    for team in teams:
        players = Player.query.filter(Player.team_id == team.id)

        for player in players:
            try:
                r = requests.get(player_stats_templ.format(player.id))
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
                    db.session.add(player)
            except Exception as e:  # NO
                print(f"Error {e} accessing player stats for player {player.id} on team {team.id}")

        db.session.commit()
