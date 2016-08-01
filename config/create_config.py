#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: create_config.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-03-27
#      History: 
#=============================================================================
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.http import HttpResponse, response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import commands,json,yaml
from assets.models import  Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import salt_api_pass, salt_api_user, salt_api_url, pxe_url_api
from assets.models import Host
import hashlib
#日志记录
from salt_ui.views.api_log_class import salt_log
#写入mongodb生成配置文件
from assets.conf_api.mongodb_api import *
#登录
from accounts.auth_login.auth_index_class import auth_login_required
import json
from salt_ui.api.salt_https_api import salt_api_jobs, pxe_api, Salt_Jobsid
import time, commands
import requests, json
from salt_ui.models import Salt_mode_name
from django import forms
from users.models import CustomUser
from django.http import HttpResponse


def select_conf_class(request):
    """
    查询当前业务服务配置文件
    """
    content = {}
    prod_name = request.GET['prod_name']
    content["server_name"] = request.GET['server_name']
    data = db.server_conf.find_one({"prod_name": prod_name})
    content["data"] = data["server"]
    content["prod_name"] = prod_name
    content.update(csrf(request))
    # print content
    return render_to_response('config/server_code_list.html', content, context_instance=RequestContext(request))