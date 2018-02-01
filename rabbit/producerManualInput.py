#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import pika
from pika import spec
import sys
credentials = pika.PlainCredentials("guest","guest")
conn_params = pika.ConnectionParameters("192.168.1.15",port=5672,credentials = credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()

channel.confirm_delivery()

'''
channel.exchange_declare(exchange='hello-exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)
'''
msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
#消息持久化了
msg_props.delivery_mode = 2

if channel.basic_publish(exchange='hello-exchange',
                         body=msg,
                         properties=msg_props,
                         routing_key='hola',
                         mandatory=True):
    print 'Confirm received!'
else:
    print 'Message lost!'

connection.close()

