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

import datetime
import os
import re
#import md5
import json
import time
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.template import RequestContext
from django.db import connection
from django.http import HttpResponse
#from salt_ui.api import salt_api
from salt_ui.models import *
from django.contrib.auth.decorators import login_required
import commands,json,yaml
import subprocess
from salt_ui.api import *
from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch, Project, System_usage
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import salt_api_token
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import  salt_api_pass,salt_api_user,salt_api_url,pxe_url_api
from django.http import HttpResponse,HttpResponseRedirect

#日志记录
from salt_ui.views.api_log_class import salt_log
#登录
# from accounts.auth_login.auth_index_class import login_required
from django.contrib.auth.decorators import login_required


class Host_from(forms.ModelForm):

    class Meta:
        model = Host
        fields = "__all__"

def select_node(ip):
    """
    查询主机是否在数据库中
    :return:
    """
    try:
        data = Host.objects.get(eth1=ip)
    except:
        return False
    return data

#判断选择了多少台主机
# @login_required
# @csrf_protect
def salt_update_node(request):
    context = {}
    update_name = request.GET['node_name']
    if request.method == 'POST':    
        uf = Host_from(request.POST)
        if uf.is_valid():   
            # 查询数据库中是否有此数据
            zw = uf.save(commit=False)
            zw.edit_username = request.user.username
            zw.status = 1
            zw.vm = int(request.POST["vm"])
            business_id = request.POST.get('business')
            if business_id:
                business = Project.objects.get(id=business_id)
                zw.business = business
            # zw.save()
            uf = Host_from()
            context['uf'] = uf
            context.update(csrf(request))
            return HttpResponseRedirect("/salt/status/")
            # return render_to_response('assets/host_list.html',context,context_instance=RequestContext(request))
        else:
            print "save error"
            uf = Host_from()
            context["server_type"] = Project.objects.all()
            context['uf'] = uf
            context.update(csrf(request))
            return HttpResponseRedirect("/salt/status/")

    if len(update_name) > 0 and Host.objects.filter(node_name=update_name).count() == 0:
        token_api_id = token_id()
        #同步本地grains
        salt_garins_sync = salt_api_token({'fun': 'saltutil.sync_all', 'tgt': update_name, 'client': 'local'}, salt_api_url, {"X-Auth-Token": token_api_id})
        salt_garins_sync.run()
        #重新加载模块
        salt_garins_reload = salt_api_token({'fun': 'sys.reload_modules', 'tgt': update_name, 'client': 'local'}, salt_api_url, {"X-Auth-Token": token_api_id})
        salt_garins_reload.run()
        #执行模块
        list = salt_api_token({'client': 'local', 'fun': 'grains.items', 'tgt': update_name, 'timeout': 100}, salt_api_url, {"X-Auth-Token": token_api_id})
        master_status = list.run()
        uf = Host_from()
        for i in master_status["return"]:
            system_os = i[update_name]["os"]
            osarch = i[update_name]["osarch"]
            ipinfo = i[update_name]["hwaddr_interfaces"]["eth0"]
            mac = ipinfo.replace(":", "-")
            if "eth0" in i[update_name]["ip_interfaces"]:
                context["eth0"] = i[update_name]["ip_interfaces"]["eth0"][0]
            elif "em1" in i[update_name]["ip_interfaces"]:
                context["eth0"] = i[update_name]["ip_interfaces"]["em1"][0]
            else:
                context["eth0"] = "127.0.0.1"
            if "eth1" in i[update_name]["ip_interfaces"]:
            # try:
                context["eth1"] = i[update_name]["ip_interfaces"]["eth1"][0]
            # except IndexError:
            else:
                context["eth1"] = False
            # ip = request.POST.get("eth1")
            # data = select_node(context["eth0"])
            try:
                data = Host.objects.get(eth1=context["eth0"])
                data.node_name = i[update_name]["fqdn"]
                data.mac = mac
                data.core_num = i[update_name]["num_cpus"]
                data.system_version = i[update_name]["osrelease"]
                data.system_cpuarch = i[update_name]["cpuarch"]
                data.cpu = i[update_name]["cpu_model"]
                data.memory = i[update_name]["mem_total"]
                data.save()
                return HttpResponseRedirect("/salt/status/")
                # return render_to_response('saltstack/node_add.html', context, context_instance=RequestContext(request))

            except:
                context["vm"] = i[update_name]["virtual"]
                context["cpu_model"] = i[update_name]["cpu_model"]
                context["mem_total"] = i[update_name]["mem_total"]
                context["update_name"] = update_name
                context["mac"] = mac
                context["system_os"] = system_os
                context["osarch"] = osarch
                context["uf"] = uf
                context["os"] = i[update_name]["os"]
                context["edit_brand"] = Server_System
                context["edit_Cores"] = Cores
                context["edit_system"] = System_os
                context["system_usage"] = System_usage
                context["edit_system_arch"] = system_arch
                context["server_type"] = Project.objects.all()
                # print context
                context.update(csrf(request))
        return render_to_response('saltstack/node_add.html', context, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/salt/status/")


