import datetime
import json
from redis import Redis
from flask import current_app
from flask_sse import Message


"""
There is a difference between the sse data and redis message.
Flask-sse encapsulates your data object into a Message object.

redis publishes to channels and flask-sse by default publishes to
channel='sse' (but you can override it).
flask-sse

To use these Message classes with flask-sse.publish you must use it like:
msg = DraftPickMessage(round, user, player)
sse.publish(msg.data, type=msg.type)
"""


def send_sse_message(msg):
    redis_url = current_app.config.get("SSE_REDIS_URL")
    # print(f"redis url from my config is: {redis_url}")
    if not redis_url:
        raise KeyError("Must set a redis connection URL in app config.")
    redis = Redis.from_url(redis_url)

    msg_json = json.dumps(msg.to_dict())
    redis.publish(channel="sse", message=msg_json)


class DraftStatusMessage(Message):
    """
    drafting_user is the user currently drafting
    next_user is the user next up to draft
    """
    def __init__(self, seq=0, state=None, round=None, draft_pos=None, draft_direction=None, 
                 draftee_count=None, drafting=None, drafting_user=None, next_user=None, users=None):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data = {
            "seq": seq,
            "ts": ts,
            "round": round,
            "state": state,
            "draft_pos": draft_pos,
            "draft_direction": draft_direction,
            "draftee_count": draftee_count,
            "drafting": drafting
        }
        if drafting_user is not None:
            data["drafting_user"] = {
                "id": drafting_user.get('id'),
                "name": drafting_user.get('display_name')
            }
        if next_user is not None:
            data["next_user"] = {"id": next_user.get('id'), "name": next_user.get('display_name')}
        if users is not None:
            data["users"] = users
        super().__init__(data, type="draft-status")


class DraftpickMessage(Message):
    # def __init__(self, draft_round, user=None, player=None, seq=None):
    def __init__(self, round=None, user=None, player=None, seq=None):
        if user is None or player is None:
            raise KeyError("user and player must be set")
        data = {
            "seq": seq,
            "round": round,
            "user": {
                "id": user.get('id'),
                "name": user.get('display_name'),
            },
            "player": {
                "id": player.id,
                "name": player.full_name,
                "team_id": player.team.id,
                "team_name": player.team.name,
                "team_abbrev": player.team.abbrev
            }
        }
        super().__init__(data, type="draft-pick")


class DraftUsersMessage(Message):
    def __init__(self, users=None):
        if users is None or not isinstance(users, list):
            raise KeyError("users must be a list of user")

        user_list = []
        for u in users:
            user_list.append(u.as_dict_public())

        data = {
            "users": user_list
        }
        super().__init__(data, type="draft-users")
