#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: jid_api.py
#         Desc: 2014-14/12/30:上午11:13
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.shortcuts import render_to_response,HttpResponseRedirect, HttpResponse
from django.template import RequestContext
import json
from salt_ui.models import salt_returns
from salt_ui.api.salt_https_api import salt_api_jobs
import ast


#判断选择了多少台主机
def salt_jid_select(request):
    s = salt_returns.objects.filter(jid=20141229171108903653).values("full_ret")

    return HttpResponse(s)