#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: rab_send.py
#         Desc: 2015-15/10/12:上午9:37
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

import pika
import time
import json

credentials = pika.PlainCredentials("admin", "voilet_850225")
# credentials = pika.PlainCredentials("cmdb", "964e486c24cfd234ca9aa63bdc3f3fab")
conn_params = pika.ConnectionParameters("192.168.111.101", credentials=credentials)
connection = pika.BlockingConnection(conn_params)

channel = connection.channel()
channel.exchange_declare(exchange='auth.user', exchange_type='direct')

channel.basic_publish(exchange='auth.user',
                      routing_key="user",
                      body=json.dumps({'ip': '192.168.121.18', 'type': 1, 'user': 'songxs', 'auth': 0,
                                       'node': 'salt_test', "uid": 3002, "gid": 1001,
                                       'ssh_key': "asdfasdfsadfasdfsadf"}))

# print " [x] Sent %r:%r" % (routing_key, message)
# time.sleep(10)
connection.close()


# import requests
# requests.packages.urllib3.disable_warnings()
# url = "https://192.168.8.80/login"
# headers = {
#                 'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
#                 "Accept": "application/json",
#             }
# data = {"username": "salt", "password": "992a15aecbcf5727df775c45a35738cf",
#         "eauth": "pam"}
# s = requests.post(url, headers=headers, data=data, verify=False)
# t = s.json()
# salt_token = [i["token"] for i in t["return"]]
# salt_token = salt_token[0]
# print salt_token
# headers["X-Auth-Token"] = salt_token
# # test = {"remove": True, "force": True}
# # salt_data = {"client": "local", "fun": "user.delete", "tgt": "salt_test", "arg": {"remove": True, "force": True}, "voilet1"}
#
# salt_data = {"client": "local", "fun": "user.delete", "tgt": "salt_test", "arg": ["remove=True", "force=True", "voilet1"]}
# # salt_data = {"client": "local", "fun": "user.delete", "tgt": "salt_test", "arg": "voilet1" }
# sl = requests.post("https://192.168.8.80/", headers=headers, data=salt_data, verify=False)
# print sl.text

#
# credentials = pika.PlainCredentials("admin", "voilet_850225")
# conn_params = pika.ConnectionParameters("192.168.111.101", credentials=credentials)
# connection = pika.BlockingConnection(conn_params)
#
# channel = connection.channel()
# channel.exchange_declare(exchange='auth.user', type='direct')
# channel.basic_publish(exchange='auth.user',
#                       routing_key="user",
#                       body="hello")
#
# result = channel.queue_declare(exclusive=True)
# queue_name = result.method.queue
#
# severities = sys.argv[1:]
# if not severities:
#     print >> sys.stderr, "Usage: %s [info] [warning] [error]" % \
#                          (sys.argv[0],)
#     sys.exit(1)
#
# for severity in severities:
#     channel.queue_bind(exchange='auth.user',
#                        queue="user",
#                        routing_key=severity)
#
# print ' [*] Waiting for logs. To exit press CTRL+C'

# def callback(ch, method, properties, body):
#     print " [x] %r:%r" % (method.routing_key, body,)
#
# channel.basic_consume(callback,
#                       queue="user",
#                       no_ack=True)
#
# channel.start_consuming()