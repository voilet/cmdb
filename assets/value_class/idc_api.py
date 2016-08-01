# !/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: idc_api.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-09-23
#      History: 
#=============================================================================
import json, time, urllib
from django.shortcuts import render_to_response,get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch, ENVIRONMENT, room_hours

from salt_ui.api.salt_token_id import *


import requests, re

def host_all():
    """
    主机列表信息
    """
    content = {"room_id": {}, "room": []}
    node_list = Host.objects.all()
    content["install_system"] = node_list.filter(business__isnull=True).count()
    content["centos_system"] = node_list.filter(system="CentOS").count()
    content["debian"] = node_list.filter(system="Debian").count()
    content["server_list_count"] = node_list.count()
    content["room_number"] = {"bumber": [i[0] for i in room_hours]}
    for i in room_hours:
        room_data = node_list.filter(room_number=i[0])
        cabinet_list = []
        cab_num = []
        for cabinet_id in room_data:
            cabinet_list.append(cabinet_id.cabinet)
        cabinet_list = list(set(cabinet_list))
        for num in sorted(cabinet_list):
            cab_num.append({"cab_num": node_list.filter(room_number=i[0], cabinet=num).count(), "cab_name": num})
        content["room"].append({"cabinet_name": i[0], "count_len": len(cabinet_list), "count": sorted(cabinet_list), "name": cab_num})
    return content
