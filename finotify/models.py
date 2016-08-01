#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2013-02-20 14:52:11
#      History:
#=============================================================================

from django import forms
from django.db import models
from uuidfield import UUIDField


class finotify(models.Model):
    """
    上报信息
    """
    uuid = UUIDField(auto=True, primary_key=True)
    file_path = models.CharField(max_length=64, blank=True, null=True, verbose_name='可疑文件')
    dangerous = models.TextField(blank=True, null=True, verbose_name='报警内容 ')
    server_ip = models.CharField(blank=True, null=True, max_length=64, verbose_name='服务器ip')
    files_create_time = models.DateTimeField(blank=True, null=True, max_length=64, verbose_name='监控时间')







