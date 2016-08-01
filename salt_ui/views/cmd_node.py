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

#import md5

from django.shortcuts import render_to_response
from django.template import RequestContext
#from salt_ui.api import salt_api
from assets.models import Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404

#日志记录
#登录
# from accounts.auth_login.auth_index_class import login_required
from django.contrib.auth.decorators import login_required

#判断选择了多少台主机
@login_required
@csrf_protect
def salt_cmd_node(request):
    context = {}
    type_node = ""
    if request.method == 'POST':
        salt_text = request.POST
        print salt_text
        service_type = salt_text.getlist("business")
        for i in service_type:
            service_name_type = get_object_or_404(Project,service_name = i)
            server_list = service_name_type.host_set.all()
            for s in server_list:
                type_node += "%s," % (s.node_name)
        context["type_node"] = type_node
        print type_node
        context.update(csrf(request))
        return render_to_response('saltstack/salt_cmd_run.html',context,context_instance=RequestContext(request))
    else:
        return render_to_response('saltstack/salt_cmd_run.html',context,context_instance=RequestContext(request))
