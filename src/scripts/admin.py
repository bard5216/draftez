import argparse
from sqlalchemy import func

from app import app
from app.models import db
from app.models import Status
from app.models import Pick
from app.models import User

status_table = [
    {"k": "current_draft_pos", "v": "1"},  # draft pos
    {"k": "round", "v": "1"},
    {"k": "draft_direction", "v": "forward"},  # forward / reverse
    {"k": "state", "v": "init"},  # init, in-progress, paused, complete
    # {"k": "draftee_count", "v": "0"},  # number of draftees
]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-I', action='store_true', help='Initialize draft')
    parser.add_argument('-v', action='count', default=0, help='Verbose')
    args = parser.parse_args()

    with app.app_context():
        if args.I:
            n = Pick.query.delete()
            print(f"{n} rows deleted from Pick")
            n = Status.query.delete()
            print(f"{n} rows deleted from Status")
            db.session.commit()

            for o in status_table:
                status = Status(**o)
                db.session.add(status)
            db.session.commit()
            print(f"{len(status_table)} rows inserted into Status")

            # funky way required by sqlalchemy to do: "select count(*) from user"
            user_count = db.session.query(func.count(User.id)).scalar()
            status = Status(k="draftee_count", v=str(user_count))
            db.session.add(status)
            db.session.commit()
            print(f"setting draftee_count to {user_count}")
