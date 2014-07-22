from celery import Celery


alarms = Celery("alarms", broker="amqp://localhost//",
                    backend= 'mongodb://localhost//'
                    )
alarms.conf.update(
    CELERY_DEFAULT_QUEUE='alarms',
    CELERY_DEFAULT_ROUTING_KEY='alarms',
    CELERY_DEFAULT_EXCHANGE='loghub',
    CELERY_TIMEZONE = 'UTC',
    CELERY_TASK_RESULT_EXPIRES = 60 * 36,
    CELERYD_CONCURRENCY = 1,
    CELERYD_PREFETCH_MULTIPLIER = 2,
    CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 4,
    CELERYD_TASK_TIME_LIMIT = 60 * 5
    )

if __name__ == '__main__':
    alarms.start()