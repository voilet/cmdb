#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from users.models import CustomUser
import time
from uuidfield import UUIDField


class MonitorHttp(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    title = models.CharField(max_length=120, verbose_name=u"监控名称")
    url = models.TextField(verbose_name=u'监控url', help_text=u'同一组服务器多个url监控换行即可')
    monitor_type = models.BooleanField(default=True, verbose_name=u'请求方式')
    monitor_ip = models.TextField(verbose_name=u'ip列表')
    mail_status = models.BooleanField(verbose_name=u"是否邮件报警", default=True)
    mail = models.TextField(verbose_name=u'邮件联系人', help_text=u'多个邮件联系人换行即可')
    weixin_status = models.BooleanField(verbose_name=u'是否微信报警', default=True)
    weixin = models.TextField(verbose_name=u'微信联系人', help_text=u'多个联系人换行即可')
    payload = models.TextField(verbose_name=u'post数据', null=True, blank=True, help_text=u'POST提交数据,需json格式')
    status = models.BooleanField(verbose_name=u'状态', default=True)
    result_code = models.BooleanField(verbose_name=u'header/code', default=True,
                                      help_text=u'默认监控http status,如果选择为返回值,则监控返回数据retCode是否为200')
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"http监控"
        verbose_name_plural = verbose_name


class MonitorHttpLog(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    monitorId = models.CharField(max_length=120, verbose_name=u"监控ID")
    monitor_title = models.CharField(max_length=120, verbose_name=u"监控名称")
    content = models.TextField(verbose_name=u"日志内容", null=True, blank=True)
    code = models.IntegerField(verbose_name=u'状态码')
    job_id = models.CharField(max_length=32, verbose_name=u'任务id')
    status = models.BooleanField(verbose_name=u'状态', default=True)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.monitor_title

    class Meta:
        verbose_name = u"http监控日志"
        verbose_name_plural = verbose_name


class MonitorMySql(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=120, verbose_name=u"监控名称")
    monitor_ip = models.TextField(verbose_name=u'ip列表')
    monitor_user = models.CharField(verbose_name=u'用户名', max_length=32, help_text=u'监控帐号')
    monitor_pass = models.CharField(verbose_name=u'用户名', max_length=128, help_text=u'监控密码')
    monitor_port = models.IntegerField(verbose_name=u'端口', help_text=u'mysql端口')
    mail = models.TextField(verbose_name=u'邮件', help_text=u'多个邮件联系人换行即可')
    weixin = models.TextField(verbose_name=u'微信', help_text=u'多个联系人换行即可')
    slave = models.BooleanField(verbose_name=u'主从', default=True)
    status = models.BooleanField(verbose_name=u'状态', default=True)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"mysql监控"
        verbose_name_plural = verbose_name
