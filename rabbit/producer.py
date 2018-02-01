#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import pika
import sys
import json
credentials = pika.PlainCredentials("guest","guest")
conn_params = pika.ConnectionParameters("192.168.1.15",port=5672,credentials = credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()

channel.exchange_declare(exchange='hello-exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

msg = json.dumps({"key1":"abc","key2":123})
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
#这里消息没有持久化
#如果需要消息持久化 那么就加上下面的配置
#msg_props.delivery_mode = 2


channel.basic_publish(exchange='hello-exchange',
                      body=msg,
                      properties=msg_props,
                      routing_key='hola')

connection.close()