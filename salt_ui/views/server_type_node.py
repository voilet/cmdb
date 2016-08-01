#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 
#      History:
#=============================================================================
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from assets.models import Project, ProjectUser,Host
#日志记录
#登录
from django.contrib.auth.decorators import login_required


