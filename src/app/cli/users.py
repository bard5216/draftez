import click
import logging
from flask import Blueprint

from app.models import (
    db,
    User,
)


bp = Blueprint("cli_users", __name__)
logger = logging.getLogger(__name__)


@bp.cli.command("create")
# @click.option('--create', is_flag=True)
@click.argument('username')
@click.option("--display", required=True)
def create_user(username, display):
    print(f"create user {username}")
    user = User(username=username, display_name=display)
    db.session.add(user)
    db.session.commit()


@bp.cli.command("update")
@click.argument('username')
@click.option("--password")
def update_user(username, password):
    user = db.session.query(User).filter(User.username == username).first()
    if user is None:
        print("User {username} does not exist")
        return

    user.password = password
    db.session.add(user)
    db.session.commit()


@bp.cli.command("list")
def list_users():
    users = db.session.query(User).order_by(User.pos).all()
    if len(users) == 0:
        print("No users")
        return

    print("{}  {:<25} {:<4} {:<16} {}".format(
        "*", "Username", "Pos", "Display name", "Password"
    ))
    print("-" * 50)
    for u in users:
        print("{}  {:<25} {:<4} {:<16} {}".format(
            "*" if u.admin else "-",
            u.username,
            u.pos,
            u.display_name,
            u.password
        ))
