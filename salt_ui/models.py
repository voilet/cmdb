#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
# =============================================================================
from django.db import models
from django import forms
from django.db import models
from users.models import CustomUser
from assets.models import Project, Host
from uuidfield import UUIDField


class salt_api_log(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    user_name = models.CharField(max_length=20, verbose_name=u"用户名")
    minions = models.CharField(max_length=2048, verbose_name=u"主机名")
    jobs_id = models.CharField(max_length=40, verbose_name=u"job", blank=True, null=True, )
    stalt_type = models.CharField(max_length=20, verbose_name=u"操作类型")
    salt_len_node = models.IntegerField(max_length=20, verbose_name=u"多少台主机执行")
    stalt_input = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"命令")
    api_return = models.TextField(verbose_name=u"执行记录")
    log_time = models.DateTimeField(auto_now=True, verbose_name=u"操作时间")

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name = u"salt操作日志"
        verbose_name_plural = verbose_name


class salt_conf(models.Model):
    """
    salt配置文件数据模型
    """
    uuid = UUIDField(auto=True, primary_key=True)
    server_name = models.CharField(max_length=20, verbose_name=u"服务名称")
    prod_name = models.CharField(max_length=20, verbose_name=u"项目名称")
    file_name = models.CharField(max_length=20, verbose_name=u"文件名")
    server_code = models.TextField(verbose_name=u"项目配置")


STATE_CHOICE = (
    (0, u"可申请"),
    (1, u"审批中"),
    (2, u"审批通过"),
)


class SetupLog(models.Model):
    """
        状态描述：一般用户申请推送状态由0到1
                admin审批＝通过状态由1到2，拒绝由1到0(用户修改，重新提交)
                一般用户执行 推送，状态由2到0
    """
    uuid = UUIDField(auto=True, primary_key=True)
    user = models.ForeignKey(CustomUser, verbose_name=u"申请人", related_name="aplly_user")
    approve_user = models.ForeignKey(CustomUser, verbose_name=u"审批人", related_name="approve_user", null=True,
                                     blank=True)
    business = models.ForeignKey(Project, verbose_name=u"申请业务")
    content = models.TextField(verbose_name=u"操作描述")
    status = models.IntegerField(verbose_name=u"申请状态", choices=STATE_CHOICE, default=0)
    approve_time = models.DateTimeField(verbose_name=u"审批时间", null=True, blank=True)
    reject_reason = models.TextField(verbose_name=u"拒绝原因", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=u"申请时间")
    run_time = models.DateTimeField(verbose_name=u"执行时间", null=True, blank=True)

    def __unicode__(self):
        return self.business.service_name

    class Meta:
        verbose_name = u"配置推送记录"
        verbose_name_plural = verbose_name


class jids(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    jid = models.CharField(unique=True, max_length=255, verbose_name=u"jid记录")
    load = models.TextField(verbose_name=u"执行结果")

    def __unicode__(self):
        return self.jid

    class Meta:
        verbose_name = u"jid"
        verbose_name_plural = verbose_name
        managed = True
        app_label = 'jids'


class salt_returns(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    fun = models.CharField(max_length=50, verbose_name=u"命令类型")
    jid = models.CharField(max_length=255, primary_key=True, verbose_name=u"操作id")
    return_field = models.TextField(db_column='return',
                                    verbose_name=u"执行结果")  # Field renamed because it was a Python reserved word.
    id = models.CharField(max_length=255, verbose_name=u"主机")
    success = models.CharField(max_length=10, verbose_name=u"状态")
    full_ret = models.TextField(u'返回数据')
    alter_time = models.DateTimeField(verbose_name=u"返回时间")

    def __unicode__(self):
        return self.jid

    class Meta:
        managed = True
        app_label = 'salt_returns'
