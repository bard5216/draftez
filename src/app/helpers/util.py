import logging
from app.models import (
    db,
    Status,
    User
)

logger = logging.getLogger(__name__)

_status_rows = [
    ('draft_pos', '1'),
    ('draft_direction', 'forward'),
    ('draftee_count', '1'),
    ('state', 'waiting'),
    ('round', '1'),
    ('drafting', '2'),
]


def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    """
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))


def get_users():
    users = User.query.all()
    u_list = [u.as_dict_public() for u in users]
    return u_list


def next_picking():
    pass


"""
Status helpers
"""


def get_status_dict():
    status_dict = {}
    rows = db.session.query(Status).all()
    status_dict = {row.k: row.v for row in rows}
    return status_dict


def get_status_item(k):
    status = db.session.query(Status).filter(Status.k == k).one()
    return status


def get_status_val(k, int_val=False):
    status = db.session.query(Status).filter(Status.k == k).one()
    logger.info(f"get_status_val: v={status.v}")
    if int_val:
        return int(status.v)
    return status.v


def get_current_round():
    status = Status.query.filter(Status.k == "round").first()
    return int(status.v)


def get_current_state():
    status = Status.query.filter(Status.k == "state").first()
    return status.v


def get_draftee_count():
    status = Status.query.filter(Status.k == "draftee_count").first()
    return int(status.v)


def get_current_draft_pos():
    """
    Return the draft position of current draftee
    """
    status = Status.query.filter(Status.k == "draft_pos").first()
    return int(status.v)


def get_draft_direction():
    status = Status.query.filter(Status.k == "draft_direction").first()
    draft_direction = status.v  # "forward" "reverse"
    return draft_direction


def get_next_drafting():
    cur_pos = get_current_draft_pos()  # pos of current drafting
    # n = get_draftee_count()
    dir = get_draft_direction()

    if dir == "forward":
        """
        In this direction cur should always be < n
        """
        next = cur_pos + 1
    else:
        next = cur_pos - 1

    return next
