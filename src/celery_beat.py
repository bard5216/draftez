import logging
from celery.schedules import crontab
from app import create_worker
from app import celery
from app.tasks.update import (
    periodic_update
)


logger = logging.getLogger(__name__)

app = create_worker()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*'),
        periodic_update.s(),
        name='Status updates',
    )
