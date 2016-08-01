#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: swan_api.py
#         Desc: 2015-15/1/5:下午1:24
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
from mysite.settings import salt_api_pass, salt_api_user, salt_api_url, pxe_url_api, Environment, swan_url
import requests
import json


# class swan_push_api(object):
#     def __init__(self, user, fqdn, url):
#         self.user = user
#         self.fqdn = fqdn
#         self.url = url
#
#         self.headers = {
#             'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
#             'Referer': 'http://salt.int.fun.com'
#         }
#
#     def run(self):
#         """执行"""
#
#         payload = {"username": self.user, "fqdn": self.fqdn}
#         return payload

def swan_push_api(data):
    url = swan_url
    headers = {
        'CustomUser-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        "Content-Type": "application/json",
    }

    choose = int(data.get("choose"))

    arg = data.get("arg")

    if choose == 2:
        url = "%sgit/" % url
    elif choose == 3:
        url = "%sjava/" % url
    elif choose == 4:
        url = "%sshell/" % url
    else:
        data = {"status": 404, "message": "接口参数错误"}
        return data
    try:
        swan_rst = requests.post(url, data=json.dumps(data), headers=headers, timeout=1)
        data = swan_rst.json()
        return data

    except:
        data = {"status": 404, "message": "接口请求失败"}
        return data
