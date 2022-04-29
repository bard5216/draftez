from celery.schedules import crontab


class CeleryConfig(object):
    # def attrs(self):
    #     return [key for key in dir(self) if key[0] != '_']

    celery_broker_url = 'redis://localhost:6380'
    result_backend = 'redis://localhost:6380'

    timezone = "America/Edmonton"
    enable_utc = False

    imports = [
        # "app.tasks.job",
        # "app.tasks.interface",
    ]

    # nothing below is referenced by make_celery
    # CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
    # CELERY_TASK_SERIALIZER = 'json'
    # CELERY_RESULT_SERIALIZER = 'json'

    # this is not used YET 
    CELERYBEAT_SCHEDULE = {
        'status_updates': {
            'task': 'app.tasks.test.print_hello',
            # Every minute
            'schedule': crontab(minute="*"),
        }
    }