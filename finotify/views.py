#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2013-02-20 14:52:11
#      History:
#=============================================================================
import json
from django.shortcuts import render_to_response
from finotify.models import  finotify
from django import forms

from assets.models import  Server_Post,Project


#提交数据
class Server_From(forms.ModelForm):
    class Meta:
        model = Server_Post


#搜索
#提交数据
class finotify_From(forms.ModelForm):
    class Meta:
        model = finotify
def shell_get(request):
    ip = request.GET['ip'].strip()
    file_path = request.GET["path"].strip()
    files_create_time = request.GET["time"].strip()
    dangerous = request.GET["dangerous"].strip()
    if request.method == 'GET':
        uf = finotify_From(request.GET)
        if uf.is_valid():
            zw = uf.save(commit=False)
            zw.server_ip = ip
            zw.file_path = file_path
            zw.dangerous = dangerous
            zw.files_create_time = files_create_time
            print ip,file_path,files_create_time,dangerous
            zw.save()
            print "is ok"
            return render_to_response('webshell.html', {'hello': 'hello word!', "id": id, "file_path": request.GET})

def index(request):
    emps = finotify.objects.order_by('-id')
    Project = Project.objects.all()
    return render_to_response(
        'hacker_list.html',
        {
        'emps':emps,
         'title':"文件监控系统－－列表页",
         'hello':'hello word!',
        'user':request.user.first_name,"name":request.user.username,
        'Project':Project,
        })

