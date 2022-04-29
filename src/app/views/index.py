import json

from flask import Blueprint, render_template, request
from app.helpers.session import current_user, login_required
from flask_sse import sse

from app.helpers.picks import get_user_picks, get_team_roster
from app.models import (
    db,
    User,
    Team
)
# from app.models import Team


index_bp = Blueprint("index", __name__, url_prefix="/")


@index_bp.route("/", methods=["GET"])
@login_required
def index():
    rosters = {}
    teams = db.session.query(Team).all()
    for t in teams:
        # rosters[t.id] = Player.query.filter(Player.team_id == t.id).order_by(Player.points.desc()).all()
        rosters[t.id] = get_team_roster(t.id)
    user_picks = {}
    users = User.query.all()
    for user in users:
        user_picks[user.display_name] = get_user_picks(user.id)
    return render_template("index.html", users=users, current_user=current_user, rosters=rosters, user_picks=user_picks, teams=teams)
    # index.html WORKS
    # return render_template("index.html", current_user=current_user)


@index_bp.route("/draftpick_notused", methods=["POST"])
def draftpick_notused():
    # selection = request.form[0]['selection']
    # pretty_print_POST(request)
    print("draftpick:")
    # print("request=", request.get_json())
    sse.publish({"message": "this is from sse"}, type="draftpick")
    return json.dumps({"message": "pick submitted"})

    player_id = request.form.get('player_id')
    print(f"draftpick: player_id={player_id}")
    # sse.publish({"user": current_user.username, "selection": selection}, type="selection")

    notice_msg = "<span>{0}</span> selected <span>{1}</span> from XXX".format(
                 current_user.display_name, player_id)
    sse.publish({"message": notice_msg}, type="notice")
    # sse.publish(notice_msg, type="notice")
    # sse.publish("placeholder", type=f"{current_user.display_name}")

    print(f"draftpick: {current_user.display_name}#{player_id}")

    # return render_template("index/draftpick.html", data=selection)
    return """<span _='on load wait 5s then set {innerText: ""} on me'>""" + player_id + " selected</span>"
