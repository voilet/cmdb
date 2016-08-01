#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: add_config_class.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-02-27
#      History: 
#=============================================================================
from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse,get_object_or_404

from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import commands,json,yaml
from assets.models import  Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf


# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from django import forms
from models import ConfTemplate



class ConfForm(forms.ModelForm):
    class Meta:
        model = ConfTemplate
        fields = "__all__"

    # def __init__(self, *args, **kwargs):
    #     super(ConfForm, self).__init__(*args, **kwargs)
    #     for one in self.fields:
    #         self.fields[one].widget.attrs.update({'class': 'form-control'})


@login_required()
def salt_conf_index(request):
    """添加配置文件"""
    conf_list = ConfTemplate.objects.filter()
    return render_to_response('config/conf_index.html', locals(), context_instance=RequestContext(request))


@login_required()
def add_conf_class(request):
    conf_list = ConfTemplate.objects.filter()
    if request.method == 'POST':
        form = ConfForm(request.POST)   
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect("/conf/list/")
    else:
        form = ConfForm()
    return render_to_response('config/add_conf.html', locals(), context_instance=RequestContext(request))


@login_required()
def edit_conf_class(request,pk):
    conf_list = ConfTemplate.objects.filter()
    conf_item = get_object_or_404(ConfTemplate,pk=pk)
    if request.method == 'POST':
        form = ConfForm(request.POST,instance=conf_item)   
        if form.is_valid(): 
            form.save()
            return HttpResponseRedirect("/conf/list/")
    else:
        form = ConfForm(instance = conf_item)
    return render_to_response('config/add_conf.html', locals(), context_instance=RequestContext(request))


@login_required()
def item_conf_class(request,pk):
    conf_list = ConfTemplate.objects.filter()
    conf_item = get_object_or_404(ConfTemplate,pk=pk)

    return render_to_response('config/item_conf.html', locals(), context_instance=RequestContext(request))


@login_required()
def list_conf_class(request):
    conf_list = ConfTemplate.objects.filter()

    return render_to_response('config/conf_list.html', locals(), context_instance=RequestContext(request))


