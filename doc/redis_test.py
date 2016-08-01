#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: redis_test.py
#         Desc: 2015-15/2/25:下午2:05
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
import requests
import yaml

salt_api_url = "https://salt-api.int.fun.tv/"
salt_api_user = "salt"
salt_api_pass = "992a15aecbcf5727df775c45a35738cf"
import redis
rc = redis.Redis(host='192.168.8.80',port=6379,db=0)
ps = rc.pubsub()

class salt_api_token(object):
    def __init__(self, data, url, token=None):
        self.data = data
        self.url = url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            "Accept": "application/x-yaml",
        }
        self.headers.update(token)

    def run(self):
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)


def token_id():
    s = salt_api_token(
        {
        "username":salt_api_user,
        "password":salt_api_pass,
        "eauth":"pam"},
        salt_api_url + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token


if __name__ == "__main__":
    token_api_id = token_id()

    list_all = salt_api_token({'fun': 'grains.item', 'tgt': "salt_test",
                               'arg': "ipv4", 'expr_form': 'list', "client": "local_async"},
                              salt_api_url, {'X-Auth-Token': token_api_id})
    list_all = list_all.run()
    jobs_id = "r_%s" % (list_all["return"][0]["jid"])
    ps.subscribe(jobs_id)   # 订阅

    for item in ps.listen():
        if item['type'] == 'message':
            print item['data']
            break

    # salt_test = salt_api_token
