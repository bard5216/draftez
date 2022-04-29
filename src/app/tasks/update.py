import logging
# from re import U
# import datetime

# from flask import current_app
from app import celery
from app.helpers.flows import calc_next_draft_pos
from app.helpers.messages import DraftStatusMessage, send_sse_message
from app.helpers.util import (
    # get_current_round,
    get_users,
    get_status_dict,
)


logger = logging.getLogger(__name__)

seq = 0


@celery.task(name='tasks.periodic_update', bind=True)
def periodic_update(self):
    global seq

    logger.info(f"periodic_update: seq={seq}")

    status = get_status_dict()
    users = get_users()

    seq = seq + 1

    next_round, next_pos, next_dir = calc_next_draft_pos(
        round=status.get('round'),
        pos=status.get('draft_pos'),
        dir=status.get('draft_direction'),
        users=users
    )

    drafting_user = None
    next_user = None
    for u in users:
        if int(u.get('pos')) == int(status.get('draft_pos')):
            drafting_user = u
        if int(u.get('pos')) == next_pos:
            next_user = u

    msg = DraftStatusMessage(
        seq=seq,
        state=status.get('state'),
        round=status.get('round'),
        draft_pos=status.get('draft_pos'),
        draft_direction=status.get('draft_direction'),
        draftee_count=status.get('draftee_count'),
        drafting=status.get('drafting'),
        drafting_user=drafting_user,
        next_user=next_user,
        users=users
    )
    send_sse_message(msg)
