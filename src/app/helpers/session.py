# import datetime
import logging
from functools import wraps
from flask import (
    # request,
    session,
    redirect,
    url_for,
    # abort,
)
# from flask.templating import render_template
from werkzeug.local import LocalProxy

# from app import appcache

logger = logging.getLogger(__name__)

# current_user = LocalProxy(lambda: get_current_user())
# current_identity = LocalProxy(lambda: get_identity())
# REMOTE_USER = LocalProxy(lambda: get_remote_user())

# current_session = LocalProxy(lambda: get_current_session())

current_user = LocalProxy(lambda: get_current_user())


def get_current_user():
    u = session.get('user', None)
    return u


def is_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # user = current_user
        # if not user.admin:
        #     abort(401)
        return f(*args, **kwargs)

    return decorated_function


def login_required(fn):
    """
    if current_user is None then the user has not logged in.
    """
    @wraps(fn)
    def decorated_fn(*args, **kwargs):
        if current_user is None:
            logger.info("User not logged in - redirecting to login page")
            return redirect(url_for('login.login'))

        logger.info("User has valid session.")

        return fn(*args, **kwargs)

    return decorated_fn
