import logging
from flask import Blueprint, render_template, request, jsonify
from flask_sse import sse

from app.models import db, User, Pick, Player, Team
from app.helpers.session import login_required, current_user
from app.helpers.messages import DraftpickMessage
from app.helpers.picks import get_user_picks, get_team_roster
from app.helpers.util import get_current_round, get_status_dict

from app.helpers.flows import draft_flow


api_bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


"""  deprecated
class DraftMsg(JSONAble):
    user_id = 0
    user_name = ""
    player_id = 0
    player_name = ""
    player_team = ""
    round = 0
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
"""


@api_bp.route("/active_users", methods=["GET"])
@login_required
def active_users():
    """
    """
    users = User.query.filter(User.active == 1).all()
    print(users)
    # u_list = [u.as_dict() for u in users]
    u_list = []
    for u in users:
        u_dict = u.as_dict_public()
        u_dict['picks'] = get_user_picks(u.id)
        u_list.append(u_dict)
    return jsonify({"results": u_list}), 200


@api_bp.route("/teams", methods=["GET"])
@login_required
def get_teams():
    teams = Team.query.order_by(Team.abbrev).all()
    team_list = [{"id": team.id, "abbrev": team.abbrev, "name": team.name, "selected": False} for team in teams]
    return jsonify({"results": team_list}), 200


@api_bp.route("/playersearch", methods=["GET"])
@login_required
def players(search=""):
    search = request.args.get("search")
    results = Player.query.filter(Player.last_name.like(f"%{search}%")).order_by(Player.last_name).all()
    return render_template("api/search_results.html", players=results)


@api_bp.route("/rosters/<team_id>")
def team_roster(team_id):
    roster = get_team_roster(team_id)
    team = {"id": team_id, "roster": roster}
    return jsonify({"results": team})


@api_bp.route("/playersearch_json", methods=["GET"])
@login_required
def players_json():
    search = request.args.get("q")
    if len(search) <= 1:
        return jsonify({"results": []}), 200
    _query = db.session.query(Player).filter(Player.last_name.ilike(f"%{search}%")).order_by(Player.points.desc())
    print(_query)
    players = _query.all()
    res = [
        {
            "full_name": p.full_name,
            "id": p.id,
            "text": f"{p.full_name} ({p.team.abbrev})",
            "games": p.games,
            "goals": p.goals,
            "assists": p.assists,
            "points": p.points,
            "team_abbrev": p.team.abbrev,
            "team_name": p.team.name,
            "team_id": p.team.id
        }
        for p in players
    ]

    return jsonify({"results": res}), 200


def get_user_by_pos(pos):
    pass


@api_bp.route("/draft_player", methods=["POST"])
def draft_player():
    """
    This has to be used by web-app only because the owner will
    be the current_user.
    """
    data = request.get_json()
    logger.info(f"/api/draftpick: data={data}")
    # print(f"current_user={current_user}")
    # print(f"current_user.id={current_user.get('id')}")

    if data['player']:
        player_data = data['player']
        player_id = player_data['id']
        player = Player.query.filter(Player.id == player_id).first()

        status = get_status_dict()

        # current_drafting is pos of current drafting
        # current_draft_pos = get_current_draft_pos()
        # user = User.query.filter(User.pos == current_draft_pos).first()

        # This establishes the users' draft pick
        pick = Pick(round=status.get('round'), user_id=current_user.get('id'), player_id=player.id)
        db.session.add(pick)
        db.session.commit()

        draft_flow(user=current_user, player=player, status=status)

        # draft_flow will advance draft_pos

        # print(f"sse-data: {msg.data}")
        # print(f"sse-type: {msg.type}")
        # sse.publish(msg.toJSON(), type="draftpick")
    else:
        pass

    logger.info("1111")
    res = {"result": {"player": player.as_dict(), "user": current_user.get('id'), "round": round}}
    logger.info("2222")
    logger.info(res)
    logger.info("3333")
 
    return jsonify(res), 200


"""
@api_bp.route("/teams/<int:team_id>/roster", methods=["GET"])
def team_roster(team_id):
    players = Player.query.filter(Player.team_id == team_id).order_by(Player.points.desc()).all()
    return render_template("partials/team_roster.html", roster=players)
"""


@api_bp.route("/picks/<int:user_id>", methods=["GET"])
def user_picks(user_id):
    """
    See app.helpers.picks.get_user_picks()

    for pick, player = db.session.query(Pick, Player).\
                                  filter(Pick.user_id==user_id).\
                                  filter(Pick.player_id==Player.id).\
                                  all():
    """

    """
    Pick.query.filter(Pick.user_id == user_id)
    select user.display_name, player.full_name, pick.round from pick
    inner join player on pick.player_id = player.id
    inner join user on pick.user_id = user.id
    """

    # picks = Pick.query.filter(Pick.user_id == user_id).order_by(Pick.round).all()
    picks = []

    return render_template("partials/user_picks.html", picks=picks)
