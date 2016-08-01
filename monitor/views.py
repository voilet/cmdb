#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: views.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/27 下午3:43
     History:   
"""

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import MonitorHttp, MonitorHttpLog
from monitor.forms import MonitorHttpForm
import json
import ast


@login_required
def HttpMonitor(request):
    """ 添加http监控 """
    if request.method == 'POST':
        uf = MonitorHttpForm(request.POST)
        if uf.is_valid():
            uf.save()
    else:
        uf = MonitorHttpForm()
    return render_to_response('monitor/httpadd.html', locals(), context_instance=RequestContext(request))


@login_required
def HttpMonitorlist(request):
    """ http监控列表 """
    data = MonitorHttp.objects.all().order_by("-createtime")
    return render_to_response('monitor/httplist.html', locals(), context_instance=RequestContext(request))


@login_required
def HttpMonitorEdit(request, uuid):
    """ http监控列表 """
    data = MonitorHttp.objects.get(pk=uuid)
    if request.method == 'POST':
        uf = MonitorHttpForm(request.POST, instance=data)
        if uf.is_valid():
            uf.save()
    uf = MonitorHttpForm(instance=data)
    return render_to_response('monitor/httpedit.html', locals(), context_instance=RequestContext(request))


@login_required
def HttpMonitorstatus(request, uuid):
    """ http监控列表 """
    data = MonitorHttp.objects.get(pk=uuid)
    data.status = int(request.GET.get("status"))
    data.save()
    return HttpResponse(json.dumps({"retCode": 200, "retMsg": "ok"}, ensure_ascii=False, indent=4))


@login_required
def HttpMonitorDel(request, uuid):
    """ http监控列表 """
    data = MonitorHttp.objects.get(pk=uuid).delete()
    return HttpResponse(json.dumps({"retCode": 200, "retMsg": "ok"}, ensure_ascii=False, indent=4))


@login_required
def HttpMonitorPage(request, uuid):
    """ http监控列表 """
    data = MonitorHttp.objects.get(pk=uuid)
    log_data = MonitorHttpLog.objects.filter(monitorId=uuid).order_by("-createtime")
    return render_to_response('monitor/httppage.html', locals(), context_instance=RequestContext(request))


def HttpMonitorApi(request):
    """ http监控列表 """
    data = MonitorHttp.objects.filter(status=True)
    result = {}
    for i in data:
        if not i.monitor_type:
            result[str(i.pk)] = {"uuid": str(i.uuid), "title": i.title, "url": i.url.split(),
                                 "monitor_type": i.monitor_type,
                                 "ip": i.monitor_ip.split(),
                                 "payload": ast.literal_eval(i.payload),
                                 "mail_status": i.mail_status, "mail": i.mail.split(),
                                 "weixin_status": i.weixin_status, "weixin": "|".join(i.weixin.split()),
                                 "result_code": i.result_code}
        else:
            result[str(i.pk)] = {"uuid": str(i.uuid), "title": i.title, "url": i.url.split(),
                                 "monitor_type": i.monitor_type,
                                 "ip": i.monitor_ip.split(),
                                 "mail_status": i.mail_status, "mail": i.mail.split(),
                                 "weixin_status": i.weixin_status, "weixin": "|".join(i.weixin.split()),
                                 "result_code": i.result_code}


    return HttpResponse(json.dumps({"retCode": 200, "retData": result, "retMsg": "ok"}), content_type = "application/json")