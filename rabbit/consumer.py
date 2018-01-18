#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import pika
import time

credentials = pika.PlainCredentials("guest","guest")
conn_params = pika.ConnectionParameters(host="192.168.1.15",port=5672,credentials = credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()

channel.exchange_declare(exchange='hello-exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

channel.queue_declare(queue="hello-queue")
channel.queue_bind(queue="hello-queue",exchange='hello-exchange',routing_key='hola')

def msg_consumer(channel,method,properties,body):
    
    #time.sleep(1)
    
    channel.basic_ack(delivery_tag=method.delivery_tag)
    #if send msg is quit then consumer script exist
    if body == "quit":
        channel.basic_cancel(consumer_tag="hello-consumer")
        channel.stop_consuming()
    else:
        print(" [x] %r:%r" % (method.routing_key, body))
    return
    
channel.basic_consume(msg_consumer, queue="hello-queue", consumer_tag="hello-consumer",)
channel.start_consuming()