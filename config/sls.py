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

from django.shortcuts import render_to_response,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django import forms
import commands,json,yaml
from assets.models import  Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import  salt_api_pass,salt_api_user, salt_api_url ,pxe_url_api
from models import Salt_mode_name
import hashlib
#日志记录
from salt_ui.views.api_log_class import salt_log
#登录
from django.contrib.auth.decorators import login_required
# from accounts.auth_login.auth_index_class import auth_login_required
from users.models import CustomUser


class SlsForm(forms.ModelForm):
    class Meta:
        model = Salt_mode_name

#服务管理
@login_required
@csrf_protect
def sls_add(request):
    content = {}
    if request.method == 'POST':    
        uf = SlsForm(request.POST)   
        # print uf
        if uf.is_valid(): 
            uf.save()
            print "server_type save is ok"
            return HttpResponseRedirect("/salt/sls/list/")
        else:
            # print "save error"
            uf = SlsForm()
            content["server_type"] = Project.objects.all()
            content['uf'] = uf
            content.update(csrf(request))
            return render_to_response('config/sls_add.html', content, context_instance=RequestContext(request))
    else:
        content["user_list"]= CustomUser.objects.all()
        content["server_type"] = Project.objects.all()
        content.update(csrf(request))
        return render_to_response('config/sls_add.html', content, context_instance=RequestContext(request))

#服务管理
@login_required
@csrf_protect
def sls_list(request):
    """
    服务包名
    """
    content = {}
    content["user_list"]= CustomUser.objects.all()
    content["server_type"] = Project.objects.all()
    sls_name = Salt_mode_name.objects.all()
    content['sls_name'] = sls_name
    content.update(csrf(request))
    return render_to_response('config/sls_list.html', content, context_instance=RequestContext(request))

#服务管理
@login_required
@csrf_protect
def sls_edit(request,id):
    content = {}
    sls_name = Salt_mode_name.objects.get(id=id)
    old_name = sls_name.sls_name

    content['sls_name'] = sls_name
    if request.method == 'POST':    
        uf = SlsForm(request.POST)   
        if uf.is_valid(): 
            sls_name.sls_name = uf.instance.sls_name
            sls_name.sls_conf = uf.instance.sls_conf
            sls_name.sls_description = uf.instance.sls_description
            sls_name.save()
            return HttpResponseRedirect("/salt/sls/list/")
        else:
            uf = SlsForm()
            content["server_type"] = Project.objects.all()
            content['uf'] = uf
            content.update(csrf(request))
            return render_to_response('config/sls_add.html', content, context_instance=RequestContext(request))
    content["user_list"]= CustomUser.objects.all()
    content["server_type"] = Project.objects.all()
    content.update(csrf(request))
    return render_to_response('config/sls_add.html', content, context_instance=RequestContext(request))

#服务管理
@login_required
@csrf_protect
def sls_del(request,id):
    content = {}
    Salt_mode_name.objects.get(id=id).delete()
    content.update(csrf(request))
    return HttpResponseRedirect("/salt/sls/list/")
