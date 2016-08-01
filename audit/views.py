#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
# =============================================================================

import json, time, urllib
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from audit.models import ssh_audit
from django.views.decorators.csrf import csrf_exempt
# 登录
from cmdb_auth.no_auth import check_auth

import requests, re


@csrf_exempt
def audit_save(request):
    """
    用户操作记录入库
    user_name = models.CharField(max_length=20, verbose_name=u'操作用户')
    bash_shell = models.TextField(verbose_name=u'命令')
    audit_data_time = models.DateTimeField(verbose_name=u'操作时间')
    server_ip = models.IPAddressField(verbose_name=u'服务器ip')
    """
    if request.method == 'POST':
        user_name = request.POST.get("user_name")
        bash_shell = request.POST.get("bash_shell")
        audit_data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        server_ip = request.POST.get("server_ip")
        # data = ssh_audit_log(user_name, bash_shell, audit_data_time, server_ip)
        ssh_audit_data = ssh_audit(user_name=user_name, bash_shell=bash_shell, audit_data_time=audit_data_time,
                                   server_ip=server_ip)
        s = ssh_audit_data.save()
        if s:
            return HttpResponse(json.dumps({"status": 200, "result": u"已入库"}, ensure_ascii=False, indent=4, ))
    return HttpResponse(json.dumps({"status": 403, "result": u"error"}, ensure_ascii=False, indent=4, ))


@csrf_exempt
def audit_list(request):
    """
    用户审计记录
    :param requests:
    :return:
    """
    status = check_auth(request, "server_audit")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    audit_data = ssh_audit.objects.all().order_by("-audit_data_time")
    return render_to_response('audit/list.html', locals(), context_instance=RequestContext(request))


@csrf_exempt
def audit_select(request):
    """
    查询服务器操作记录
    """
    # ip = "192.168.8.225"
    if request.method == 'POST':
        ip = request.POST.get("ip")
        try:
            audit_page = int(request.POST.get("num"))
        except:
            audit_page = 0
        if audit_page > 0:
            num = audit_page
            audit_data = ssh_audit.objects.filter(server_ip=ip).order_by("-audit_data_time")[:num]
        else:
            audit_data = ssh_audit.objects.filter(server_ip=ip).order_by("-audit_data_time")

        data = []
        for i in audit_data:
            # content[ip]
            data.append({"bash_shell": "%s  %s     %s" % (i.user_name, i.audit_data_time, i.bash_shell)})
        # print data

        return HttpResponse(json.dumps({"status": 200, "result": data}, ensure_ascii=False, indent=4), content_type="application/json")

    return HttpResponse(json.dumps({"status": 403, "result": "error"}, ensure_ascii=False, indent=4), content_type="application/json")
