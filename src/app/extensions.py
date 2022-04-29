from celery import Celery
from flask_migrate import Migrate
from flask_session import Session

migrate = Migrate()
flask_session = Session()  # use flask_session, not session, otherwise will collide with Flask.session
celery = Celery(__name__)