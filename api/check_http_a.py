#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: check_http.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/28 下午8:27
     History:   
"""

import sys, socket, select, struct, logging, smtplib, httplib, time, requests, urllib
import threading
from urlparse import urlparse
from email.MIMEText import MIMEText
import requests
from multiprocessing import Process, Queue, Pool
import os, time, random
import json

# config
log_file_name = '%s.log' % sys.argv[0]
wx_message = []
monitor_api = "http://127.0.0.1:8000/api/monitor/http/"

url_timeout = 20
mailhost = 'mail.funshion.com'
mailuser = 'im@funshion.com'
mailpasswd = 'funshion321#@!'

mail_error_to = ['songxs@fun.tv', "guojy@fun.tv", "zhangzhang@fun.tv"]
mail_subject_prefix = '北京机房'
weixin_url = "http://192.168.111.101:8888/"

s = requests.get(monitor_api)
result = s.json()

url_list = result.get("retData")

logger = logging.getLogger()
hdlr = logging.FileHandler(log_file_name, 'w')
formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)


class HttpApi(threading.Thread):
    # def __init__(self, **kwargs,url, ip, args):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.data = kwargs
        self.result = self.data.get("args")
        self.url = self.data.get("url")
        o = urlparse(self.url)
        self.hostname = o.hostname
        self.ip = self.data.get("ip")
        self.payload = self.result.get("payload")
        self.mail_status = self.result.get("mail_status")
        self.mail = self.result.get("mail")
        self.weixin_status = self.result.get("weixin_status")
        self.weixin = self.result.get("weixin")
        self.title = self.result.get("title")
        self.result_code = self.result.get("result_code")
        self.status = self.result.get("monitor_type")

        if o.port:
            self.port = o.port
        else:
            self.port = 80

        if o.query == '':
            if o.path == '':
                self.request = '/'
                self.path = '/'
            else:
                self.request = o.path
                self.path = o.path
        else:
            self.request = o.path + '?' + o.query
        self.path = o.path

    def run(self):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36",
                "Connection": "close",
                "Accept-Encoding": "gzip, deflate",
                "Host": self.hostname,
                "Cache-Control": "no-cache",
            }

            http = httplib.HTTPConnection(self.ip, self.port, timeout=url_timeout)
            if not self.status:
                params = urllib.urlencode(json.loads(self.payload))
                http.request("POST", self.request, params, headers)
            else:
                http.putrequest("GET", self.request, 1, 1)
                http.putheader("User-Agent",
                               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36")
                http.putheader("Connection", "close")
                http.putheader("Accept-Encoding", "gzip, deflate")
                http.putheader("Host", self.hostname)
                http.putheader("Cache-Control", "no-cache")
                http.endheaders()  # endheaders()执行时才会开始建立尝试建立连接

            r = http.getresponse()
            print r.read()
            if not r:
                logger.error(
                        "%s-%s:%s Fatal Error: http.getresponse(), impossible? %s" % (
                            self.hostname, self.ip, self.port, self.title))

                message = "%s %s:%s Response: '%s %s '%s" % (
                    self.hostname, self.ip, self.port, r.status, r.reason,
                    self.title)

                if self.weixin_status:
                    send = SendWeixin(user=self.weixin, message=message)
                    send.push()

            if r.status == 408:
                logger.info("%s-%s:%s Response: '%s %s'" % (self.hostname, self.ip, self.port, r.status, r.reason))

            elif r.status >= 400:
                logger.error(
                        "%s%s-%s:%s Response: '%s %s' %s" % (
                            self.hostname, self.path, self.ip, self.port, r.status, r.reason,
                            self.title))
                message = "%s %s:%s Response: '%s %s '%s" % (
                    self.hostname, self.ip, self.port, r.status, r.reason,
                    self.title)

                if self.weixin_status:
                    send = SendWeixin(user=self.weixin, message=message)
                    send.push()

            elif r.status == 301 or r.status == 302:
                self.redirect = r.getheader('location')
                logger.info("%s-%s:%s Response: '%s %s'. Location: %s" % (
                    self.hostname, self.ip, self.port, r.status, r.reason, self.redirect))
            else:
                logger.info("%s-%s:%s Response: '%s %s'" % (self.hostname, self.ip, self.port, r.status, r.reason))
                # message = "%s %s:%s Response: '%s %s '%s" % (
                #     self.hostname, self.ip, self.port, r.status, r.reason,
                #     self.title)
                #
                # if self.weixin_status:
                #     send = SendWeixin(user=self.weixin, message=message)
                #     send.push()

        except Exception, e:
            logger.info("%s-%s:%s Fatal Error: %s" % (self.hostname, self.ip, self.port, e))


class WebServer(threading.Thread):
    def __init__(self, **kwargs):
        threading.Thread.__init__(self)
        self.data = kwargs
        self.url = self.data.get("url")
        self.ips = self.data.get("ips")
        self.args = self.data.get("args")

        # 以下代码可将当前dns解析vip一同加入检测
        """
        try:
            addrs = socket.getaddrinfo(urlparse(self.url).hostname, 'http', socket.AF_INET, socket.SOCK_STREAM)
        except Exception, e:
            logger.error("%s-%s, need check dns server." % (urlparse(self.url).hostname, e))
            addrs = []
        for addr in addrs:
            ip = addr[4][0]
            if ip in self.ips:
                pass
            else:
                self.ips.append(ip)
        """

    def run(self):
        threads = []
        # 每个ip建立一个线程
        for ip in self.ips:
            g = HttpApi(url=self.url, ip=ip, args=self.args)
            threads.append(g)

        # 依次启动所有线程
        for thread in threads:
            thread.start()

        # 等待所有线程退出
        for thread in threads:
            thread.join()


class Mail(object):
    def __init__(self, filename, subject_prefix=''):
        self.fromaddr = mailuser
        self.toaddrs = ''
        self.mailtype = 'ALL'
        self.filename = filename
        self.subject = ''
        self.wxmessage = ''
        self.subject_prefix = subject_prefix

    def sendmail(self, toaddrs, mailtype):
        f = open("%s" % self.filename, 'r')
        text = f.readlines()
        f.close()
        message = ''
        if mailtype == 'ERROR':
            error_num = 0
            for line in text:
                if line.find('ERROR') >= 0:
                    message += line
                    error_num += 1
                    wx_message.append(line)

            self.subject = '%s服务异常！%s/%s' % (self.subject_prefix, error_num, len(text))
        else:
            self.subject = '%s服务检查日志: %s' % (self.subject_prefix, len(text))
            for line in text:
                message += line

        msg = MIMEText(message)
        msg['From'] = self.fromaddr
        msg['To'] = ','.join(toaddrs)
        msg['Subject'] = self.subject
        if len(message) != 0:
            try:
                server = smtplib.SMTP(mailhost)
                server.login(mailuser, mailpasswd)
                server.sendmail(self.fromaddr, toaddrs, msg.as_string())
                server.quit()
            except Exception, e:
                logger.error(e)


class SendWeixin(object):
    def __init__(self, **kwargs):
        self.user = kwargs.get("user")
        self.message = kwargs.get("message")

    def push(self):
        data = {
            "user": self.user,
            "message": self.message,
            "token": "8d7e1693e9ad674f645b87032a66169a"
        }
        rst = requests.post(weixin_url, data=data)
        print rst.json()
        return True


def sendmail():
    # SendMail
    m = Mail(log_file_name, mail_subject_prefix)
    # m.sendmail(mail_error_to, 'ERROR')


def main():
    threads = []

    for domains in url_list.keys():
        ips = url_list[domains]["ip"]
        for domain in url_list[domains]["url"]:
            g = WebServer(url=domain, ips=ips, args=url_list[domains])
            threads.append(g)

    # 依次启动所有线程
    for thread in threads:
        thread.start()

    # 等待所有线程退出
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
    # sendmail()
