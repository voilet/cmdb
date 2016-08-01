#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zhanglei'

from django.db import models
from users.models import CustomUser
import time
from uuidfield import UUIDField


class ConfTemplate(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=30, verbose_name=u"模板名称")
    init_file = models.TextField(verbose_name=u'初始文件')
    template_file = models.TextField(verbose_name=u'模板文件')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"模板文件"
        verbose_name_plural = verbose_name
        app_label = "assets"


class OperationLog(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    user = models.ForeignKey(CustomUser, verbose_name=u"操作人", related_name="operate_user")
    content = models.TextField(verbose_name=u"操作描述")
    mail_list = models.TextField(verbose_name=u"周知名单", null=True, blank=True, help_text="多个邮件以逗号分隔,周知人为空则发送运维组，平台架构组")
    mail_title = models.CharField(verbose_name=u"标题", max_length='100')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"申请时间")
    mail_status = models.BooleanField(default=True, help_text=u"邮件发送是否成功")

    def mail_content(self):
        return self.user.username + "\r\n" + self.content

    def save(self, *args, **kwargs):
        super(OperationLog, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = u"操作记录"
        verbose_name_plural = verbose_name
        app_label = "salt_ui"


class Salt_mode_name(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    sls_name = models.CharField(max_length='20', verbose_name=u'软件包名')
    sls_description = models.TextField(blank=True, null=True, verbose_name=u"描述")
    sls_conf = models.IntegerField(blank=True, null=True, default=0, verbose_name=u"是否需要配置文件")

    def __unicode__(self):
        return self.sls_name

    class Meta:
        verbose_name = u"rpm包名"
        verbose_name_plural = verbose_name
        app_label = 'salt_ui'
