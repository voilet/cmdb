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
from users.models import CustomUser
from django.db import models
from assets.models import Host


manager_demo = [(i, i) for i in (u"经理", u"主管", u"项目责任人", u"管理员", u"BOOS")]
Department = [(u"ops", u"plat", u'dev')]
auth_id = [(u"普通用户", u"普通用户"), (u"管理员", u"管理员")]
auth_gid = [(1001, u"运维部"), (1002, u"架构"), (1003, u"研发"), (1004, u"测试")]



class UserCreateForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'email', 'department', 'mobile', "user_key")





