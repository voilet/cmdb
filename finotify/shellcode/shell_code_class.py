#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
#=============================================================================

import json
from django.shortcuts import render_to_response
from finotify.models import  hacker_url,naxsi_hacker
from django import forms
from assets.models import  Server_Post,Project
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from decimal import *
#提交数据
class Server_From(forms.ModelForm):
    class Meta:
        model = Server_Post


#搜索
#提交数据
class hacker_from(forms.ModelForm):
    class Meta:
        model = hacker_url

def shell_code_post(request):
    if request.method == 'POST':
        print request.POST
        uf = hacker_from(request.POST)
        # print "*" * 20
        # if uf.is_valid():
        #     uf.save()
        # else:
        #     print "is over"
        # return render_to_response('error.html',{})
    return render_to_response('error.html',{})
@login_required(None)
def hacker_index(request):
    emps = hacker_url.objects.order_by('-id')
    Project = Project.objects.all()
    return render_to_response(
        'hacker_web.html',
        {
        'contacts':emps,
         'title':"入侵上报－－列表页",
         'hello':'hello word!',
        'user':request.user.first_name,"name":request.user.username,
        'Project':Project,
        },context_instance=RequestContext(request))


#naxsi 上报提交数据
class naxsi_hacker_from(forms.ModelForm):
    class Meta:
        model = naxsi_hacker

def naxsi_code_post(request):
    if request.method == 'POST':
        print request.POST
        uf = naxsi_hacker_from(request.POST)
        # print uf
        # print "*" * 20
        if uf.is_valid():
            uf.save()
            # print "is ok"
        else:
            print "is over"
        return render_to_response('error.html',{})
    return render_to_response('error.html',{})

# class hack_code_bili(object):
#     def __init__(self,hack_exp_code):
#         self.hack_exp_code = hack_exp_code

@login_required(None)
def naxsi_hacker_index(request):
    emps = naxsi_hacker.objects.order_by('-id')
    Project = Project.objects.all()
    return render_to_response(
        'naxsi_hacker_web.html',
        {
        'contacts':emps,
         'title':"naxsi拦截上报－－列表页",
         'hello':'hello word!',
        'user':request.user.first_name,"name":request.user.username,
        'Project':Project,
        },context_instance=RequestContext(request))

#图形展示

@login_required(None)
def naxsi_hacker_count(request):
    #查询表里面总数据
    emps = naxsi_hacker.objects.order_by('-id')
    naxsi_count =  emps.count()
    sql_count =  emps.filter(type_attack="sql").count()
    xss_count = emps.filter(type_attack="xss").count()
    rfi_count = emps.filter(type_attack="rfi").count()
    upload_count = emps.filter(type_attack="upload").count()
    EVADE_count = emps.filter(type_attack="EVADE").count()
    TRAVERSAL_count = emps.filter(type_attack="TRAVERSAL").count()
    if sql_count !=0:
        sql_count =  round(Decimal(sql_count) / Decimal(naxsi_count) * 100,2)
    if xss_count !=0:
        xss_count =  round(Decimal(xss_count) / Decimal(naxsi_count) * 100,2)

    if rfi_count !=0:
        rfi_count =  round(Decimal(rfi_count) / Decimal(naxsi_count) * 100,2)

    if upload_count !=0:
        upload_count =  round(Decimal(upload_count) / Decimal(naxsi_count) * 100,2)

    if EVADE_count !=0:
        EVADE_count =  round(Decimal(EVADE_count) / Decimal(naxsi_count) * 100,2)

    if TRAVERSAL_count !=0:
        TRAVERSAL_count =  round(Decimal(TRAVERSAL_count) / Decimal(naxsi_count) * 100,2)

    # print naxsi_count
    return render_to_response(
        'hacker_web_bingtu.html',
        {
         'title':"naxsi攻击类型比例",
         'hello':'hello word!',
        'user':request.user.first_name,"name":request.user.username,
        # 'naxsi_count':naxsi_count,
        'sql_count':sql_count,
        'xss_count':xss_count,
        'rfi_count':rfi_count,
        'naxsi_count':naxsi_count,
        'upload_count':upload_count,
        'EVADE_count':EVADE_count,
        'TRAVERSAL_count':TRAVERSAL_count
        },context_instance=RequestContext(request))