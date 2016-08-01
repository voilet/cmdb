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
from django.shortcuts import HttpResponse, render_to_response
from django import forms
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf

from assets.models import  Host,IDC,Server_System,Cores,System_os,system_arch,Project,System_usage
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import salt_api_url

#日志记录
#登录
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required

class Host_from(forms.ModelForm):
    # FAVORITE_COLORS_CHOICES = Project.objects.values_list("id","service_name")
    # print FAVORITE_COLORS_CHOICES
    # business = forms.MultipleChoiceField(required=False,
    #     widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)
    class Meta:
        model = Host
        fields = "__all__"

@login_required
@csrf_protect
def server_update(request,id):
    """
    更新上报数据
    """
    context = {}
    edit_id = Host.objects.get(id=id)
    token_api_id = token_id()
    list_all = salt_api_token(
    {
    'client': 'local_async',
    'fun': 'grains.items',
    'tgt': edit_id.node_name,
                   },
    salt_api_url,
    {"X-Auth-Token": token_api_id}
    )
    list_all = list_all.run()
    for i in list_all["return"]:
        try:
            context["jid"] = i["jid"]
            context["minions"] = i["minions"]
        except KeyError:
            return render_to_response('assets/update_error.html', context, context_instance=RequestContext(request))
    jobs_id = context["jid"]
    jobs_url = salt_api_url + "/jobs/" + jobs_id
    minions_list_all = salt_api_jobs(
    jobs_url,
    {"X-Auth-Token": token_api_id}
    )
    voilet_test = minions_list_all.run()
    for i in voilet_test["return"]:
        update_keys = i.keys()
        try:
            update_key = update_keys[0]
        except IndexError:
            return render_to_response('assets/update_error.html', context, context_instance=RequestContext(request))
        context["cmd_run"] = i[update_key]
    # context["eth0"] = context["cmd_run"]["ip_interfaces"]["eth0"][0]
    # try:
    #
    if "eth0" in context["cmd_run"]["ip_interfaces"]:
        edit_id.eth1 = context["cmd_run"]["ip_interfaces"]["eth0"][0]
    elif "em1" in context["cmd_run"]["ip_interfaces"]:
        edit_id.eth1 = context["cmd_run"]["ip_interfaces"]["em1"][0]
    else:
        edit_id.eth1 = "127.0.0.1"
    if "eth1" in context["cmd_run"]["ip_interfaces"]:
    # try:
        edit_id.eth2 = context["cmd_run"]["ip_interfaces"]["eth1"][0]
    # except IndexError:
    else:
        edit_id.eth2 = ""
    edit_id.memory = context["cmd_run"]["mem_total"]
    edit_id.core_num = int(context["cmd_run"]["num_cpus"])
    edit_id.system = context["cmd_run"]["os"]
    edit_id.system_version = context["cmd_run"]["lsb_distrib_release"]
    edit_id.cpu = context["cmd_run"]["cpu_model"]
    edit_id.save()
    #日志入库
    return HttpResponse('<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button><h4>数据更新完成,三秒后关闭</h4></div>')
    # return render_to_response('assets/update.html', context, context_instance=RequestContext(request))


