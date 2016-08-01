#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: api.py
#         Desc: 2015-15/1/19:下午10:44
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
import requests
import json
import pika
import datetime


class uerdel(object):
    """pxe api接口"""

    def __init__(self, user, fqdn, url):
        self.user = user
        self.fqdn = fqdn
        self.url = url

        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'http://salt.int.fun.com'
        }

    def run(self):
        """执行"""

        payload = {"username": self.user, "fqdn": self.fqdn}
        return payload


class RabApi(object):
    """pxe api接口"""

    def __init__(self, **kwargs):
        self.host = "192.168.111.101"
        self.user = "cmdb"
        self.password = "964e486c24cfd234ca9aa63bdc3f3fab"
        self.x_name = 'auth.user'
        self.q_name = 'user'

        self.data = kwargs

    def SendMessage(self):
        credentials = pika.PlainCredentials(self.user, self.password)
        conn_params = pika.ConnectionParameters(self.host, credentials=credentials)
        connection = pika.BlockingConnection(conn_params)

        channel = connection.channel()
        channel.exchange_declare(exchange=self.x_name, type='direct')

        data = self.data.get("args")

        channel.basic_publish(exchange=self.x_name,
                              routing_key=self.q_name,
                              body=json.dumps(data))
        connection.close()
        return True


if __name__ == '__main__':
    s = {'node': u'l-message12118.tv.prod.ctc', 'gid': 1001, 'user': u'songxs', 'ip': u'192.168.121.18', 'type': 1,
         'ssh_key': u'AAAAB3NzaC1yc2EAAAABIwAAAQEApG9ojMiz/CRlfAPVoIsU+YI6U7rSWGYiBUcnE8wc4rL3r7gQ9e2DtTRsDqIoyPHU/+KDE+LnM5c/a64HI+SQg+wEmiwFbjw3V1hvCqbZBv7SdLSV+0VlZP6tVlPvWwV4s4IEoB5Ji6FY7NLVV7HF72MVnrGDXOirzZhAHhtzAeTchQI7Y7JnExkSQtUdlREklhgYvdiu98QahffNT4W8VeLAtkhvjpVAH0uNE5TYjsiBvibtGxSI1jQGW6X+2IuudaQuMjp+tS/1fHoCgj00/HJnblCiwlwh2O00f70665RaBJSTl5gOKjgRurNfT5H9wi6ZALX+8cGAlRn2ZRG+lw==',
         'auth': 0, 'uid': 3002}
    a = RabApi(args=s)
    print a.SendMessage()


def Date_time():
    now_time = datetime.datetime.now()
    old_time = now_time - datetime.timedelta(days=1)
    start_time = datetime.datetime.strptime(old_time.strftime('%Y-%m-%d'), '%Y-%m-%d')
    stop_time = datetime.datetime.strptime(now_time.strftime('%Y-%m-%d'), '%Y-%m-%d')

    return start_time, stop_time

