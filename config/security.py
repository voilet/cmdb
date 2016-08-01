# !/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: security.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-08-11
#      History: 
#=============================================================================
from django.shortcuts import render_to_response,get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from users.models import CustomUser

from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch
from assets.models import Project, System_usage, Service,Line,ProjectUser
import ast

def hacker_select(node_list, project, user):
    """
    过滤是否有非常传参
    """

    status = True

    business_item = Project.objects.get(service_name=project)
    user_all = CustomUser.objects.get(username=user)
    form_user = ProjectUser.objects.get(project=business_item, user=user_all)

    user_auth_ok = {"user": "", "status": "False", "env": [], "node": []}

    if user_all == form_user.user:
        user_auth_ok["user"] = user_all.username
        user_auth_ok["status"] = True
        user_auth_ok["env"] = ast.literal_eval(form_user.env)

    host_list = Host.objects.filter(business=business_item)
    for node in host_list:
        if node.env in user_auth_ok["env"]:
            user_auth_ok["node"].append(node.node_name)

    for i in node_list:
        if i not in user_auth_ok["node"]:
            status = False
            break

    return status