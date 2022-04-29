# # import click
# import logging
# import time
# from flask import Blueprint, current_app
# from redis import Redis
# from sqlalchemy import func

# from app.models import (
#     db,
#     User,
# )
# from app.helpers.util import (
#     get_status_val,
#     get_current_state,
#     get_current_round,
#     get_next_drafting
# )


# bp = Blueprint("cli_monitor", __name__)
# logger = logging.getLogger(__name__)


# @bp.cli.command()
# # @click.option('--create', is_flag=True)
# # @click.argument('userid', required=False)
# def monitor():
#     # redis = Redis.from_url(current_app.config.get("SSE_REDIS_URL"))

#     min_query = db.session.query(func.min(User.id))
#     user = db.session.query(User).filter(User.id.in_(min_query)).first()
#     logger.info(f"Starting user is {user.username}")

#     seq = 0
#     while True:
#         seq += 1
#         current_pos = get_status_val("current_drafting")
#         # current_drafting = get_current_drafting()
#         next_drafting = get_next_drafting()
#         logger.info(f"draft_monitor: current_drafting={current_pos}, next_drafting={next_drafting}")
#         time.sleep(5)
