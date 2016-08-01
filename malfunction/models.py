#!/usr/bin/env python
#   -*- coding: utf-8 -*-
#   =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
#   =============================================================================

from django.db import models
from uuidfield import UUIDField
from DjangoUeditor.models import UEditorField

malf_status = (
    (0, u"处理中"),
    (1, u"未处理"),
    (2, u"关闭"),
)

source_data = (
    (0, u"zabbix"),
    (1, u"nagios"),
    (2, u"cacti"),
    (3, u"smokeping"),
    (4, u"监控脚本"),
    (5, u"监控宝"),
    (6, u"其它"),
)

grade_data = (
    (0, u"高危"),
    (1, u"严重"),
    (2, u"中级"),
    (3, u"一般"),
    (4, u"无影响"),
)


class Incident(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    title = models.CharField(max_length=256, verbose_name=u'标题')
    ip = models.IPAddressField(blank=True, null=True, verbose_name=u'ip')
    url = models.TextField(blank=True, null=True, verbose_name=u'URL')
    projectuser = models.CharField(max_length=32, verbose_name=u'业务负责人',
                                   help_text=u'业务维护人员,输入中文名称')
    closeuser = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'故障处理人员')
    # type = models.IntegerField(verbose_name=u"机房类型", choices=source_data, max_length=32, blank=True, null=True)
    source = models.IntegerField(choices=source_data, max_length=4, verbose_name=u'报障来源')
    starttime = models.DateTimeField(verbose_name=u'发生时间')
    scantime = models.DateTimeField(verbose_name=u'发现时间', blank=True, null=True, )
    stoptime = models.DateTimeField(blank=True, null=True, verbose_name=u'结束时间')
    # mailcomment = models.TextField(blank=True, null=True, verbose_name=u'报警内容')
    mailcomment = UEditorField(u'报警内容', width=800, height=300, filePath="", upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, blank=True)
    # status = models.BooleanField(default=0, verbose_name=u'关闭')
    status = models.IntegerField(verbose_name=u"处理状态", choices=malf_status, max_length=32, default=1)
    classical = models.BooleanField(default=0, verbose_name=u'设为案例')
    grade = models.IntegerField(verbose_name=u'故障等级', max_length=64, blank=True, null=True, choices=grade_data)
    # comment = models.TextField(blank=True, null=True, verbose_name=u'处理过程')
    comment = UEditorField(u'处理过程', width=800, height=300, filePath="", upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, blank=True, default="")
    project_principal = models.CharField(verbose_name=u'项目负责人', max_length=32, null=True, blank=True, default="",
                                         help_text=u"如需要邮件通知项目负责人,请填写项目负责人邮箱")
    incident_user = models.CharField(max_length=32, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        managed = True
        db_table = 'incident'
        verbose_name = u"故障管理"
        verbose_name_plural = verbose_name
