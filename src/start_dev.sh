# This is the preferred way to start a dev environment for puckluck.
# See docs/gunicorn.txt for reason why.
#
# Start appserver:
echo "############################################"
echo "#"
echo "#  Is redis running?"
echo "#  Start with:"
echo "#    redis-server --port 6380"
echo "#"
echo "############################################"

gunicorn --worker-class gevent --bind 127.0.0.1:8000 'app:create_app()'


# Start celery beat handler
celery -A celery_beat.celery beat --loglevel=info


# Start celery worker handler
celery -A celery_beat.celery worker --loglevel=debug

