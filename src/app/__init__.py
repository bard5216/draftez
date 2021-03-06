import logging
import os
from flask import (
    Flask,
    redirect,
    url_for,
    g,
    request,
    session,
)
from flask_cors import CORS
from flask_sse import sse
# from flask_assets import Bundle, Environment

# from config import Config
from celeryconfig import CeleryConfig

from app.middleware import PrefixMiddleWare
from app.extensions import (
    celery,
    migrate,
    flask_session,
)
from app.models import db


logger = logging.getLogger(__name__)


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    flask_session.init_app(app)


def register_blueprints(app):
    from .cli.draftpick import bp as cli_draftpick_bp
    from .views.admin import admin_bp
    from .views.index import index_bp
    from .views.login import login_bp
    from .views.api import api_bp
    from .cli.admin import bp as cli_admin_bp
    from .cli.pop import bp as cli_pop_bp
    from .cli.users import bp as cli_users_bp
    # from .cli.monitor import bp as cli_monitor_bp

    app.register_blueprint(cli_draftpick_bp, cli_group=None)
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(sse, url_prefix="/stream")
    app.register_blueprint(cli_admin_bp, cli_group="admin")
    app.register_blueprint(cli_pop_bp, cli_group="populate")
    app.register_blueprint(cli_users_bp, cli_group="users")
    # app.register_blueprint(cli_monitor_bp, cli_group=None)


def init_celery(app):
    logger.debug("init_celery")

    celery.conf.update(app.config)
    celery.conf.broker_url = CeleryConfig.celery_broker_url
    celery.conf.result_backend = CeleryConfig.result_backend
    celery.conf.timezone = CeleryConfig.timezone
    celery.conf.enable_utc = CeleryConfig.enable_utc
    celery.conf.imports = CeleryConfig.imports
    # celery.conf.task_routes = CeleryConfig.task_routes

    class ContextTask(celery.Task):
        # automatically push Flask app_context()
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def create_app():
    if os.environ.get('FLASK_ENV', 'production') == 'production':
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s, %(funcName)s:%(lineno)s - %(message)s',
        level=log_level
    )
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG', default='config.DevelopmentConfig'))

    register_extensions(app)
    register_blueprints(app)

    app.wsgi_app = PrefixMiddleWare(app.wsgi_app, prefix=app.config.get('SCRIPT_NAME'))

    """
    assets = Environment(app)
    # All Bundle paths are relative to your app???s static directory, or the static directory of a Flask blueprint.
    js = Bundle('jquery.js', 'base.js', 'widgets.js',
                filters='jsmin', output='gen/packed.js')
    assets.register('js_all', js)
    """

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.before_request
    def before_request():
        if '/login/' in request.path:
            return

        if '/static/' in request.path:
            return

        user = session.get('user', None)
        if user is None:
            logger.info("@before_request: user is not logged in")
            return redirect(url_for('login.login'))

        if 'current_user' not in g:
            g.current_user = user

    return app


def create_worker():
    if os.environ.get('FLASK_ENV', 'production') == 'production':
        log_level = logging.INFO
    else:
        log_level = logging.DEBUG

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s, %(funcName)s:%(lineno)s - %(message)s',
        level=log_level
    )
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG', default='config.DevelopmentConfig'))

    register_extensions(app)
    init_celery(app)

    return app
