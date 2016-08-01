# !/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: salt_highstate.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-07-14
#      History: 
#=============================================================================
from django.shortcuts import render_to_response, HttpResponse
from django.template import RequestContext
from salt_ui.api.salt_token_id import *
from mysite.settings import auth_key, salt_api_url, websocket_url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
import hashlib
import time



@login_required
@csrf_exempt
def salt_highstate(request):
    if request.method == 'POST':
        data = request.POST.copy()
        arg = data.get("project")
        node_list = data.getlist("node_name")
        token_api_id = token_id()

        # 选择cmd类型执行方法
        list_all = salt_api_token({'fun': 'state.sls', 'tgt': node_list, 'expr_form': 'list', "client": "local_async",
                                   'arg': arg}, salt_api_url, {'X-Auth-Token': token_api_id})
        list_all = list_all.run()
        result = list_all["return"][0]
        token = hashlib.sha1(request.user.username + auth_key + arg + time.strftime('%Y-%m-%d',
                                     time.localtime(time.time()))).hexdigest()
        jid = result.get('jid', False)

        if jid:
            return HttpResponse(json.dumps({"status": 200, "jid": jid, "name": arg, "token": token},
                                           ensure_ascii=False, indent=4))

        return HttpResponse(json.dumps({"status": 403, "jid": jid, "token": token, "name": arg},
                                       ensure_ascii=False, indent=4))

        # return render_to_response('autoinstall/salt_highstate.html', locals(), context_instance=RequestContext(request))



@login_required
def JobsJid(request):
    """
    :param request:
    :return:
    """
    jid = request.GET.get("jid")
    name = request.GET.get("name")
    oldtoken = request.GET.get("token")
    token = hashlib.sha1(request.user.username + auth_key + name + time.strftime('%Y-%m-%d',
                        time.localtime(time.time()))).hexdigest()

    if token == oldtoken:
        websocket_status = True
        web_socket_url = websocket_url
        return render_to_response('autoinstall/websocket.html', locals(), context_instance=RequestContext(request))
    websocket_status = False
    return render_to_response('autoinstall/websocket.html', locals(), context_instance=RequestContext(request))
