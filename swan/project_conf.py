#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: project_conf.py
#         Desc: 2014-14/12/31:上午11:38
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse,get_object_or_404
from django.http import HttpResponse, response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import commands,json,yaml
from assets.models import  Project
from salt_ui.models import project_swan, swan_pro, swan_port
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.core.context_processors import csrf


# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from django import forms
from config.models  import ConfTemplate

class swan_form(forms.ModelForm):
    """
    """
    choose = forms.ChoiceField(widget=forms.RadioSelect, choices=swan_pro, required=True, initial=0, label=u"发布类型" )
    class Meta:
        model = project_swan
        fields = [
            "choose",
            "salt_sls",
            "script",
            "tgt",
            ]

# class MessageForm(EmbeddedDocumentForm):
#       class Meta:
#           document = test_config
#           # embedded_field_name = 'messages'
#           fields = ['shop_name', "address"]

class swan_all_form(forms.ModelForm):
    """
    sadf
    """
    check_port_status = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_port, required=True, initial=0, label=u"是否检测端口" )
    choose = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_pro, required=True, initial=1, label=u"发布类型" )
    bat_push = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_port, required=True, initial=0, label=u"批量发布")

    class Meta:
        model = project_swan
        fields = [
            "choose",
            "config_name",
            "salt_sls",
            "bat_push",
            "check_port_status",
            "check_port",
            ]

# @csrf_exempt
def project_add(request,id):
    """

    :param request:
    :return:
    """
    sid = id
    env = request.GET.get("env")
    item = Project.objects.get(id=id)
    if env == "default":
        uf = swan_form()
        env = "default"

    else:
        # uf = MessageForm()
        uf = swan_all_form()
        env = "all"


    if env == "default":
        if request.method == 'POST':    
            uf = swan_form(request.POST)   
            if uf.is_valid(): 
                zw = uf.save(commit=False)
                zw.project_name = item.aliases_name
                zw.project_id = item.id
                zw.check_port = 0
                zw.save()

            return HttpResponseRedirect("/assets/server/type/list/")

    else:
        if request.method == 'POST':    
            uf = swan_all_form(request.POST)   
            if uf.is_valid():   
                zw = uf.save(commit=False)
                zw.project_name = item.aliases_name
                zw.project_id = item.id
                zw.save()

                return HttpResponseRedirect("/assets/server/type/list/")
    return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))