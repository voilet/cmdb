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
from users.models import CustomUser
from uuidfield import UUIDField


class ssh_audit(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    user_name = models.CharField(max_length=20, verbose_name=u'操作用户')
    bash_shell = models.TextField(verbose_name=u'命令')
    audit_data_time = models.DateTimeField(verbose_name=u'操作时间')
    server_ip = models.IPAddressField(verbose_name=u'服务器ip')

    def __unicode__(self):
        return self.user_name

    class Meta:
        verbose_name = u"审计"
        verbose_name_plural = verbose_name
