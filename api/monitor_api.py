#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: monitor.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/2/1 上午11:01
     History:   
"""

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from monitor.forms import MonitorLogForm
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def HttpMonitorLog(request):
    """ http监控列表 """
    if request.method == 'POST':
        uf = MonitorLogForm(request.POST)
        if uf.is_valid():
            zw = uf.save(commit=False)
            zw.status = int(request.POST.get("status"))
            zw.save()
    return HttpResponse(json.dumps({"retCode": 200, "retMsg": "ok"}, ensure_ascii=False, indent=4))
