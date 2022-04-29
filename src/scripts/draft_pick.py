"""
Perform a draft pick
"""
import datetime
import sys
from redis import Redis
from flask import current_app, json  # stream_with_context
from app.helpers.messages import DraftpickMessage

from app import app
from app.models import User, Player


def main():
    user_id = sys.argv[1]
    round = sys.argv[2]
    player_id = sys.argv[3]

    redis_url = current_app.config.get("SSE_REDIS_URL")
    if not redis_url:
        raise KeyError("Must set a redis connection URL in app config.")
    redis = Redis.from_url(redis_url)

    user = User.query.filter(User.id == user_id).one()
    print(user)
    player = Player.query.get(player_id)
    message = DraftpickMessage(round, user, player)
    msg_json = json.dumps(message.to_dict())
    ts_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{ts_now}:  publishing {msg_json}")
    redis.publish(channel="sse", message=msg_json)


if __name__ == '__main__':
    argc = len(sys.argv)
    # print(f"argc={argc}")

    if argc != 4:
        print(f"Usage {sys.argv[0]} <userid> <round> <playerid>")
        sys.exit(1)

    with app.app_context():
        main()
