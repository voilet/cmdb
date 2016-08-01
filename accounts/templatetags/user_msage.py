#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: user_msage.py
#         Desc: 2015-15/2/10:下午3:26
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
from django import template
from accounts.models import CustomUser
from users.models import department_Mode
from malfunction.models import Incident

from swan.models import Apply
register = template.Library()

@register.filter(name='message')
def message(user):
    user_info = CustomUser.objects.get(username=user)
    incident = Incident.objects.filter(status=False).count() + Incident.objects.filter(projectuser=user_info.first_name, status=False).count()
    user_message = incident
    try:
        user_group = department_Mode.objects.get(pk=user_info.department_id)
        if user_group.desc_gid == 1001:
            user_message += Apply.objects.filter(op=user_info.first_name, status=2).count()

        if user_group.desc_gid == 1003:
            user_message += Apply.objects.filter(applyer=user_info.first_name, status=0).count()

        if user_group.desc_gid == 1004:
            user_message += Apply.objects.filter(qa=user_info.first_name, status=1).count()
    except:
        pass

    return user_message

@register.filter(name='swanmessage')
def swanmessage(user):
    user_info = CustomUser.objects.get(username=user)
    user_message = 0
    try:
        user_group = department_Mode.objects.get(pk=user_info.department_id)
        if user_group.desc_gid == 1001:
            user_message += Apply.objects.filter(op=user_info.first_name, status=2).count()

        if user_group.desc_gid == 1003:
            user_message += Apply.objects.filter(applyer=user_info.first_name, status=0).count()

        if user_group.desc_gid == 1004:
            user_message += Apply.objects.filter(qa=user_info.first_name, status=1).count()
    except:
        pass

    return user_message

@register.filter(name="Bell")
def Bell(user):
    num = 8
    return num


