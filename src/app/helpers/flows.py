"""
Multi event flows:

Drafting:
1. User submits a selection
"""

import logging
from flask_sse import sse

from app.helpers.util import (
    get_users,
    get_status_dict,
)
from app.helpers.messages import DraftpickMessage


logger = logging.getLogger(__name__)


def draft_flow(user=None, player=None, status=None):
    """
    User <user.id> drafts player <player.id>
    """
    if status is None:
        status = get_status_dict()

    msg = DraftpickMessage(user=user, player=player, round=status.get('round'))

    print(f"sending message: {msg}")
    sse.publish(msg.data, type=msg.type)


def calc_next_draft_pos(round=None, pos=None, dir=None, users=None):
    """
    pos: draft position of current user, 1 - count
    dir: 'forward' or 'reverse'
    users: users_dict
    count: number of users

    returns:
    round, pos, dir
    """
    if users is None:
        users = get_users()

    user_count = len(users)

    assert pos is not None and dir is not None and round is not None

    pos = int(pos)
    round = int(round)

    if dir == "forward":
        if pos < user_count:
            next_pos = pos + 1
        else:
            next_pos = pos
            dir = reverse
            round += 1
    else:
        if pos > 1:
            next_pos = pos - 1
        else:
            next_pos = 1
            dir = "forward"
            round += 1

    return round, next_pos, dir
