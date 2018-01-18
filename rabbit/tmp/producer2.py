#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import pika
from pika import spec
import sys
credentials = pika.PlainCredentials("guest","guest")
conn_params = pika.ConnectionParameters("192.168.1.15",port=5672,credentials = credentials)
connection = pika.BlockingConnection(conn_params)


def confirm_handler(frame):
    if type(frame.method) == spec.Confirm.SelectOk:
        print "Channel in 'confirm' mode"
    elif type(frame.method) == spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print "message lost"
    elif type(frame.method) == spec.Basic.Ack:
        if frame.method.delivery_tag in msg_ids:
            print "Confirm received"
            msg_ids.remove(frame.method.delivery_tag)

#connection.add_on_connection_unblocked_callback(callback_method=confirm_handler)
channel = connection.channel()
channel.confirm_delivery(callback = confirm_handler)


channel.exchange_declare(exchange='hello-exchange',
                         exchange_type='direct',
                         passive=False,
                         durable=True,
                         auto_delete=False)

msg = sys.argv[1]
msg_props = pika.BasicProperties()
msg_props.content_type = "text/plain"
msg_ids = []

a = channel.basic_publish(exchange='hello-exchange',
                          body=msg,
                          properties=msg_props,
                          routing_key='hola')
print a
msg_ids.append(len(msg_ids) + 1)
connection.close()

'''
#!/usr/bin/env python
#_*_ coding:utf-8 _*_
import sys
import pika
from  pika import spec
credentials=pika.PlainCredentials("guest","guest")

conn_params=pika.ConnectionParameters("192.168.192.129",port=5672,credentials = credentials)
conn_broker=pika.BlockingConnection(conn_params)
channel=conn_broker.channel()
 
def confirm_handler(frame):
    if type(frame.method)==spec.Confirm.SelectOk:
        print("Channel in 'confirm' mode.")
    elif type(frame.method)==spec.Basic.Nack:
        if frame.method.delivery_tag in msg_ids:
            print("Message lost")
    elif type(frame.method)==spec.Basic.Ack:
        if frame.method.delivery_tag in msg_ids:
            print("Confirm received!")
            msg_ids.remove(frame.method.delivery_tag)
 

channel.confirm_delivery(callback=confirm_handler)
#channel.confirm_delivery()
 
msg=sys.argv[1]
msg_props=pika.BasicProperties()
msg_props.content_type="text/plain"

msg_ids=[]

if channel.basic_publish(body=msg,exchange="hello-exchange",properties=msg_props,routing_key="hola"):
    print("Message recived")
else:
    print("Message lost")
#msg_ids.append(len(msg_ids)+1)
channel.close()
'''
