#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: send_test.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/6 下午11:39
     History:   
"""

import pika
import json


credentials = pika.PlainCredentials("admin", "voilet_850225")
conn_params = pika.ConnectionParameters("192.168.111.101", credentials=credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='auth.user', exchange_type='direct')

channel.basic_publish(exchange='auth.user',
                      routing_key="user",
                      body=json.dumps({'node': u'l-message12118.tv.prod.ctc', 'gid': 1001, 'user': u'songxs', 'ip': u'192.168.121.18', 'type': 1, 'ssh_key': u'AAAAB3NzaC1yc2EAAAABIwAAAQEApG9ojMiz/CRlfAPVoIsU+YI6U7rSWGYiBUcnE8wc4rL3r7gQ9e2DtTRsDqIoyPHU/+KDE+LnM5c/a64HI+SQg+wEmiwFbjw3V1hvCqbZBv7SdLSV+0VlZP6tVlPvWwV4s4IEoB5Ji6FY7NLVV7HF72MVnrGDXOirzZhAHhtzAeTchQI7Y7JnExkSQtUdlREklhgYvdiu98QahffNT4W8VeLAtkhvjpVAH0uNE5TYjsiBvibtGxSI1jQGW6X+2IuudaQuMjp+tS/1fHoCgj00/HJnblCiwlwh2O00f70665RaBJSTl5gOKjgRurNfT5H9wi6ZALX+8cGAlRn2ZRG+lw==', 'auth': 0, 'uid': 3005}))


connection.close()


#
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#         host='localhost'))
# channel = connection.channel()
#
# channel.queue_declare(queue='hello')
#
# channel.basic_publish(exchange='',
#                       routing_key='hello',
#                       body='Hello World!')
# print(" [x] Sent 'Hello World!'")
# connection.close()