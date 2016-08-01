# !/usr/bin/env jm-python27
#-*- coding: utf-8 -*-
__author__ = 'zhanglei'

import requests



class jmmail(object):
    def __init__(self, to,  subject, content, mail_cc="",):
        self.to = to
        content = "%s\n%s" % (content, u"<br><h3 style=\"color:red\">saltstack系统自动发送，请勿回复</h3>")
        self.subject = subject
        self.content = content
        self.mail_cc = mail_cc
        self.headers = {
            'CustomUser-agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        }

    def run(self):
        mail_data = {"mail_to": self.to, "mail_cc": self.mail_cc, "mail_sub": self.subject, "mail_body": self.content}
        try:
            req = requests.post("asdfasdf", data=mail_data, headers=self.headers)
            return_data = req.json()
        except:
            return_data = {"status": 503, "alert": "timeout"}
        return return_data
