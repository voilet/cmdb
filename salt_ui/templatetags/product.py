# !/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: product.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-06-15
#      History: 
#=============================================================================
from datetime import datetime

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404

from assets.models import  Project
from salt_ui.api.salt_token_id import *
from mysite.settings import salt_api_url, pxe_url_api
from assets.models import Host

#日志记录
#登录
from accounts.auth_login.auth_index_class import auth_login_required
from salt_ui.api.salt_https_api import pxe_api
import requests, json
from config.models import Salt_mode_name
from salt_ui.models import SetupLog
from assets.models import Line
from django import forms
from django.http import HttpResponse


import datetime
from django import template

register = template.Library()

@auth_login_required
def auto_index(request):
    content = {}
    line_list = Line.objects.filter()
    content["line_list"] = line_list
    content.update(csrf(request))
    if "jumeiops" in request.user.department or "admin" in request.user.department:
        return content
    else:
        return content

register.inclusion_tag('autoinstall/install_setup_list.html', takes_context=True)(auto_index)