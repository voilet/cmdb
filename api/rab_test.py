#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: rab_test.py
#         Desc: 2015-15/10/12:上午9:24
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

import pika


def callback_a(ch, method, properties, body):
    print "Queue  %r %s" % (body)


# credentials = pika.PlainCredentials("cmdb", "964e486c24cfd234ca9aa63bdc3f3fab")
credentials = pika.PlainCredentials("admin", "voilet_850225")
conn_params = pika.ConnectionParameters("192.168.111.101", credentials=credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='amq.direct', type='direct')
channel.basic_consume(callback_a,
                  queue="user",
                  no_ack=True)
channel.start_consuming()

