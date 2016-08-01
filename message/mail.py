#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: message.py
#         Desc: 2015-15/2/10:下午5:42
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

import json, time, urllib
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
#登录
from django.contrib.auth.decorators import login_required
from swan.models import Apply
from accounts.models import CustomUser
from users.models import department_Mode


@login_required
def mail(request):
    """
    站内信
    """
    user = request.user.username
    user_info = CustomUser.objects.get(username=request.user.username)
    user_group = department_Mode.objects.get(pk=user_info.department_id)
    if user_group.desc_gid == 1001:
        user_message = Apply.objects.filter(op=user_info.first_name, status__gt=2)

    if user_group.desc_gid == 1003:
        user_message = Apply.objects.filter(applyer=user_info.first_name, status__gt=0)

    if user_group.desc_gid == 1004:
        user_message = Apply.objects.filter(qa=user_info.first_name, status__gt=1)

    return render_to_response('message/message.html', locals(), context_instance=RequestContext(request))


@login_required
def new_mail(request):
    """
    站内信
    """
    user = request.user.username
    user_info = CustomUser.objects.get(username=request.user.username)
    try:
        user_group = department_Mode.objects.get(pk=user_info.department_id)
        if user_group.desc_gid == 1001:
            user_message = Apply.objects.filter(op=user_info.first_name, status=2)

        if user_group.desc_gid == 1003:
            user_message = Apply.objects.filter(applyer=user_info.first_name, status=0)

        if user_group.desc_gid == 1004:
            user_message = Apply.objects.filter(qa=user_info.first_name, status=1)
    except:
        pass

    return render_to_response('message/new_message.html', locals(), context_instance=RequestContext(request))