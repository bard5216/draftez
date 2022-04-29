# Not used.
# Could use to start appserv with gunicorn:
# gunicorn --worker-class gevent --bind 127.0.0.1:8000 wsgi

from app import create_app


application = create_app()

