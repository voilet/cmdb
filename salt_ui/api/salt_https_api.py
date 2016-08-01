#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 
#      History:
# =============================================================================

import urllib2, cookielib, urllib, yaml, json
import requests

requests.packages.urllib3.disable_warnings()


class salt_api_token(object):
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
            "Accept": "application/x-yaml",
        }
        s = {'expr_form': 'list', "client": "local_async"}
        self.headers.update(token)
        self.data.update(s)

    def run(self):
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)

    def CmdRun(self):
        self.data["client"] = "local"
        req = requests.post(self.url, headers=self.headers, data=self.data, verify=False)
        context = req.text
        return yaml.load(context)


class salt_api_jobs(object):
    def __init__(self, url, token=None):
        self.url = url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            "Accept": "application/x-yaml",
        }
        self.headers.update(token)

    def run(self):
        context = urllib2.Request(self.url, headers=self.headers)
        resp = urllib2.urlopen(context)
        context = resp.read()
        return yaml.load(context)


class pxe_api(object):
    """pxe api接口"""

    def __init__(self, data, pxe_url):
        self.data = data
        self.url = pxe_url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
            'Referer': 'http://auto.optools.int.jumei.com'
        }

    def run(self):
        """执行"""
        try:
            pxe_content = requests.post(self.url, data=self.data, headers=self.headers)
        except requests.ConnectionError:
            pxe_content_data = {'status': 110, 'result': u"pxe接口请求失败,请通知管理员检查接口请况"}
            return json.dumps(pxe_content_data)
        pxe_content_data = pxe_content.text
        print pxe_content
        return pxe_content_data


class pxe_api_delete(object):
    """通知pxe删除接口"""

    def __init__(self, mac, pxe_url):
        self.data = mac
        self.url = pxe_url
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        }

    def run(self):
        pxe_content = requests.post(self.url, data=self.data)
        pxe_content_data = pxe_content.text
        return pxe_content_data


class Salt_Jobsid(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        content = {}
        for i in self.data["return"]:
            content["jid"] = i["jid"]
        return content
