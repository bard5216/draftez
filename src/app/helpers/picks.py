# from app.models import db
from app.models import (
    Pick,
    Player
)


def get_user_picks(user_id):
    picks = Pick.query.filter(Pick.user_id == user_id).order_by(Pick.round).all()
    a = []

    round = 0
    for pick in picks:
        a.append(pick.as_dict())
        round += 1

    while round < 10:
        a.append({"round": round + 1})
        round += 1

    # print(f"get_user_picks: user_id={userid}, round={round}")
    return a


def get_team_roster(team_id):
    players = Player.query.filter(Player.team_id == team_id).order_by(Player.points.desc()).all()
    roster = []
    for p in players:
        d = p.as_dict()  # player as dict
        # change None to '-'
        for k in d.keys():
            if d[k] is None:
                d[k] = '-'
        roster.append(d)
    return roster

