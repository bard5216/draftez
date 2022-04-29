import click
import logging
from flask import Blueprint

# from app.models import (
#     db,
# )


bp = Blueprint("cli_draftpick", __name__)
logger = logging.getLogger(__name__)


@bp.cli.command()
# @click.option('--create', is_flag=True)
@click.argument('player_id', required=True)
def draftpick(player_id):
    pass
