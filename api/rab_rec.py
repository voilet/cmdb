#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: rab_rec.py
#         Desc: 2015-15/10/12:上午9:38
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History:
# =============================================================================

import json, time, os
import requests

requests.packages.urllib3.disable_warnings()
import pika
import multiprocessing, Queue


class ApiRun(object):
    """
    list_all = salt_api_token({'fun': 'cmd.run', 'tgt': node_list,
                                       'arg': cmd    },
                                      salt_api_url, {'X-Auth-Token' : token_api_id})
    """

    def __init__(self, data, url, token=None):
        self.data = data
        self.url = url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            "Accept": "application/json",
        }
        s = {'expr_form': 'list', "client": "local"}
        self.headers.update(token)
        self.data.update(s)

    def run(self):
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.json()
        return context


class SaltApi(object):
    """pxe api接口"""

    def __init__(self, **kwargs):
        self.user = "salt"
        self.password = "123455"
        self.url = "https://192.168.111.101/"
        self.data = kwargs

        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'http://salt.int.fun.com',
            "Accept": "application/json",
        }

    def token_id(self):
        s = ApiRun({
            "username": self.user,
            "password": self.password,
            "eauth": "pam"
        },
            self.url + "login",
            {}
        )

        test = s.run()
        salt_token = [i["token"] for i in test["return"]]
        salt_token = salt_token[0]
        return salt_token

    def UserAdd(self):
        """
        添加用户
        :return: 返回执行状态
        """
        self.data.get("fun")
        self.data.get("node")
        auth = self.data.get("auth")
        list_all = ApiRun({'fun': self.data.get("fun"), 'tgt': self.data.get("node"), 'arg': self.data.get("arg")},
                          self.url, {'X-Auth-Token': self.data.get("token")})

        list_all = list_all.run()
        result = list_all["return"][0]
        if int(auth) == 1:
            group_data = ["admin", self.data.get("user")]
            list_all = ApiRun({'fun': "group.adduser", 'tgt': self.data.get("node"), 'arg': group_data},
                              self.url, {'X-Auth-Token': self.data.get("token")})

            list_all.run()
        return result

    def UserDel(self):
        """
        通知salt删除用户
        :return:
        """
        list_all = ApiRun({'fun': self.data.get("fun"), 'tgt': self.data.get("node"), 'arg': self.data.get("arg")},
                          self.url, {'X-Auth-Token': self.data.get("token")})

        list_all = list_all.run()
        result = list_all["return"][0]
        return result


class Producer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # print "进行循环"
            self.queue.put("voilet")


class Consumer(multiprocessing.Process):
    def __init__(self, queue):
        multiprocessing.Process.__init__(self)
        self.queue = queue

    def run(self):
        # credentials = pika.PlainCredentials("admin", "voilet_850225")
        credentials = pika.PlainCredentials("cmdb", "sadfsadfsdf")
        conn_params = pika.ConnectionParameters("192.168.111.101", credentials=credentials)
        connection = pika.BlockingConnection(conn_params)

        channel = connection.channel()
        channel.exchange_declare(exchange='auth.user', exchange_type='direct')
        # channel.exchange_declare(exchange='auth.user', type='direct')
        channel.basic_consume(callback_a,
                              queue="user",
                              no_ack=True)
        channel.start_consuming()


def callback_a(ch, method, properties, body):
    try:
        data = json.loads(body)
        salt_token = SaltApi()
        s = salt_token.token_id()
        if int(data.get("type")) == 1:
            print "开始执行"
            gid = "gid=%s" % data.get("gid")
            uid = "uid=%s" % data.get("uid")
            home = "home=/home/users/%s" % data.get("user")
            get_user = SaltApi(fun="user.info", user=data.get("user"),
                               node=data.get("node"), token=s,
                               arg=data.get("user"), auth=data.get("auth"))
            result = get_user.UserAdd()
            if len(result.get(data.get("node"))) > 0:
                print "用户已存在"
            else:
                print "添加新用户"
                auth_data = SaltApi(fun="user.add",
                                    user=data.get("user"),
                                    node=data.get("node"),
                                    token=s,
                                    auth=data.get("auth"),
                                    arg=[data.get("user"), home, gid, uid, "shell=/bin/bash"])
                auth_data.UserAdd()
                print " user add"
                ssh_key_add = SaltApi(fun="ssh.set_auth_key",
                                      node=data.get("node"),
                                      token=s,
                                      auth=data.get("auth"),
                                      arg=[data.get("user"),
                                           data.get("ssh_key"),
                                           "enc='ssh-rsa'",
                                           "config='.ssh/authorized_keys'"]
                                      )

                print ssh_key_add.UserAdd()
        else:
            auth_data = SaltApi(fun='user.delete', node=data.get("node"), token=s,
                                arg=["remove=True", "force=True", data.get("user")])
            print auth_data.UserDel()
            print "del user"

    except ValueError, e:
        print e


# create queue
queue = multiprocessing.Queue(10)

if __name__ == '__main__':
    # main()
    # create processes
    processed = []
    for i in range(10):
        # processed.append(Producer(queue))
        processed.append(Consumer(queue))

    # start processes
    for i in range(len(processed)):
        processed[i].start()

    # join processes
    for i in range(len(processed)):
        processed[i].join()
