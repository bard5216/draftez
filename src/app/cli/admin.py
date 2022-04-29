import click
import logging
from flask import Blueprint

from app.models import (
    db,
    Status,
    User,
)


bp = Blueprint("cli_admin", __name__)
logger = logging.getLogger(__name__)

status_dict = {
    'draft_pos': ('1', 'Current position in draft order of person picking.'),
    'draft_direction': ('forward', 'forward or reverse'),
    'draftee_count': ('1', 'len(Users)'),
    'state': ('predraft', 'State of App: predraft, open, postdraft'),
    'drafting': ('', 'user.id of person currently drafting.'),
    'round': ('1', 'Current draft round. 1 - rounds'),
    'rounds': ('10', 'Number of draft rounds.'),
}


def clean_status():
    rc = db.session.query(Status).delete()
    print(f"Deleting {rc} rows from Status table")
    db.session.commit()


def initstatus():
    # clean()
    rc = db.session.query(Status).delete()
    print(f"Deleting {rc} rows from Status table")
    db.session.commit()

    for k in status_dict.keys():
        v = status_dict.get(k)
        db.session.add(Status(k=k, v=v[0]))

    db.session.commit()

    users = db.session.query(User).all()
    item = db.session.query(Status).filter(Status.k == "draftee_count").one()
    item.v = len(users)
    db.session.add(item)
    db.session.commit()


@bp.cli.command('status')
@click.option('--list', is_flag=True)
@click.option('--init', is_flag=True)
@click.option('--clean', is_flag=True)
def status(list, init, clean):
    if init:
        initstatus()
        return
    if clean:
        clean_status()
        return

    status = db.session.query(Status).all()
    if len(status) == 0:
        print("Status table empty!")
        return

    print("{:<20} {:<10} {}".format(
        "k", "v", "description"
    ))
    print("-" * 50)
    for s in status:
        print("{:<20} {:<10} {}".format(
            s.k,
            s.v,
            status_dict.get(s.k)[1]
        ))


@bp.cli.command('open')
def open_draft():
    item = db.session.query(Status).filter(Status.k == 'state').first()
    if item is None:
        print("Status table not initialized.")
        return
    if item.v != "predraft":
        print(f"Was expecting current state to be predraft but is {item.v} so skipping.")
        return
    item.v = "open"
    db.session.add(item)

    user = db.session.query(User).filter(User.pos == 1).first()
    if user is None:
        print("No user with User.pos == 1")
        return

    item = db.session.query(Status).filter(Status.k == "drafting").one()
    item.v = user.id
    db.session.add(item)

    db.session.commit()

    print(f"Setting status to open and drafting to {user.id} ({user.username})")
