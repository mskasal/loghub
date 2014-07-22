from celery import Celery

logs = Celery("logs", broker="amqp://localhost//",
                    backend= 'mongodb://localhost//'
                    )

logs.conf.update(
    CELERY_DEFAULT_QUEUE='logs',
    CELERY_DEFAULT_ROUTING_KEY='logs',
    CELERY_DEFAULT_EXCHANGE='loghub',
    CELERY_TIMEZONE = 'UTC',
    CELERY_TASK_RESULT_EXPIRES = 60 * 36,
    CELERYD_CONCURRENCY = 4,
    CELERYD_PREFETCH_MULTIPLIER = 2,
    CELERYD_TASK_SOFT_TIME_LIMIT = 60 * 4,
    CELERYD_TASK_TIME_LIMIT = 60 * 5
    )


if __name__ == '__main__':
    logs.start()