#!/usr/bin/env python
# -*- coding: utf-8 -*-

from makecelery import celery
import time

@celery.task()
def add_together(a, b):
    time.sleep(120)
    return a + b