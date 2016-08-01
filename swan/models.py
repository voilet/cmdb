# coding:utf-8

import datetime
from django.db import models
from users.models import CustomUser
from assets.models import Project
from uuidfield import UUIDField


class Apply(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    applyer = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"申请人")
    project_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"项目名")
    module_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"模块名")
    module_type = models.PositiveIntegerField(blank=True, null=True, verbose_name=u"是否有参数")
    module_tgt = models.CharField(max_length=50, blank=True, null=True, verbose_name=u"参数值")
    qa = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"测试人员")
    op = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"运维人员")
    comment = models.TextField(blank=True, null=True, verbose_name=u"备注")
    status = models.PositiveIntegerField(blank=True, null=True, verbose_name=u'状态')
    u"""
    status
    0   申请状态
    1   测试完成
    2   发布完成
    """
    date_added = models.DateTimeField(auto_now=True, default=datetime.datetime.now(), null=True, verbose_name=u"仓建时间")
    date_one = models.DateTimeField(null=True, verbose_name=u"测试完成时间")
    date_ended = models.DateTimeField(null=True, verbose_name=u"发布时间")

    def __unicode__(self):
        return self.applyer


class SwanLog(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    username = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"发布人")
    userID = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"发布人id")
    project_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"项目名")
    project_uuid = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"项目id")
    swan_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u"swan name")
    module_name = models.CharField(max_length=200, blank=True, null=True, verbose_name=u"模块名")
    module_args = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"是否有参数")
    status = models.BooleanField(verbose_name=u'发布状态', default=0)
    message = models.TextField(verbose_name=u'日志', blank=True, null=True)
    update_log = models.TextField(verbose_name=u'更新记录', blank=True, null=True)
    swan_datetime = models.DateTimeField(auto_now=True, default=datetime.datetime.now(), null=True,
                                         verbose_name=u"发布时时")

    def __unicode__(self):
        return self.project_name

    class Meta:
        managed = True
        verbose_name = u"发布日志"
