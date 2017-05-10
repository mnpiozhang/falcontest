#!/usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery
from a import app
# integrate celery
def make_celery(app):
    celery = Celery(app.name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

# Initialize Celery
celery = make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b