#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import random
import time
from flask import Flask, request, render_template, session, flash, redirect,url_for, jsonify
from utils import make_celery
#from utils import add_together



app = Flask(__name__)
#app.config['SECRET_KEY'] = 'top-secret!'

# Celery configuration
app.config['CELERY_BROKER_URL'] = 'redis://192.168.188.129:9379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://192.168.188.129:9379/0'
'''
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
'''

# Initialize Celery
celery = make_celery(app)

@celery.task()
def add_together(a, b):
    time.sleep(120)
    return a + b


@app.route('/')
def hello_world():
    #res = add_together.apply_async(args=[10, 20])
    res = add_together.apply_async(args=[10, 20])
    print app.name
    print res.id
    #return 'Hello, World!'
    return jsonify({'task_id':res.id,'result_state':'0'}), 200

