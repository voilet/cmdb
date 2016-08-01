#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: service.py
#         Desc: 2015-15/4/23:下午9:26
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import commands, json, yaml
from assets.models import Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import auth_key, websocket_url
import hashlib, time
from assets.models import Line, Service, Host, IDC, ENVIRONMENT


@login_required
def ztree_service(request):
    """
    树请求验证
    :param request:
    :return:
    """
    business_name = request.GET.get("name")
    get_token = str(request.GET.get("token"))
    service_tag = request.GET.get("service")
    sum_token = str(hashlib.sha1(request.user.username + auth_key + service_tag + time.strftime('%Y-%m-%d',
                                                                                                time.localtime(
                                                                                                    time.time()))).hexdigest())

    bus_data = Project.objects.get(service_name=request.GET.get("name"))
    service_all = Service.objects.get(name=service_tag)
    server_list = service_all.host_set.filter(business=bus_data).order_by("create_time")

    ztree_data = ztree_tag(request.user.username)

    content_status = True
    ztree_open = business_name
    if get_token != sum_token:
        content_status = False

        return render_to_response('ztree/service.html', locals(), context_instance=RequestContext(request))

    return render_to_response('ztree/service.html', locals(), context_instance=RequestContext(request))


def ServiceStatus(request, uuid):
    """
    重启服务
    :param request:
    :return:
    """
    uuid = str(uuid)
    salt_arg = request.GET.get("status")
    if request.method == 'POST':
        service_name = Service.objects.get(uuid=uuid)
        node_list = request.POST.getlist("node_name")

        ztree_data = ztree_tag(request.user.username)

        if salt_arg == "_restart":
            salt_arg = "restart"
        if salt_arg == "_reload":
            salt_arg = "reload"
        if salt_arg == "_stop":
            salt_arg = "stop"
        if salt_arg == "_start":
            salt_arg = "start"
        if salt_arg == "_status":
            salt_arg = "status"

        salt_fun = "service.%s" % (salt_arg)

        token_api_id = token_id()

        list_all = salt_api_token({'fun': salt_fun, 'tgt': "salt-master", 'client': 'local_async',
                                   'arg': service_name.name, 'expr_form': 'list'},
                                  salt_api_url, {'X-Auth-Token': token_api_id})
        list_all = list_all.run()
        jid = list_all['return'][0].get("jid")
        websocket = websocket_url
        fqdn_sum = len(node_list)

        content = {"status": 200, "msg": "is ok"}
        return render_to_response('ztree/service_websocket.html', locals(), context_instance=RequestContext(request))

    content = {"status": 403, "msg": "is over"}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


def ztree_tag(username):
    """

    :param username:
    :return:
    """

    ztree_data = []

    RootTree_data = Line.objects.all().order_by("sort")
    RooTree_Items = Project.objects.all().order_by("sort")
    iplist = []
    idle_list = []

    for i in RootTree_data:
        tree_uuid = str(i.uuid)

        token = hashlib.sha1(username + auth_key + tree_uuid + time.strftime('%Y-%m-%d',
                                                                             time.localtime(time.time()))).hexdigest()

        ztree_data.append({"id": tree_uuid, "pId": -99, "status": 1, "name": i.name, "token": token, "t": i.name,
                           "uuid": tree_uuid, 'dep': True, "open": True,
                           # "icon": "/static/img/zTreeStyle/img/diy/8.png",
                           })
    for i in RooTree_Items:
        try:

            tree_uuid = str(i.line.uuid)
            token = hashlib.sha1(username + auth_key + str(i.uuid) + time.strftime('%Y-%m-%d',
                                                                                   time.localtime(
                                                                                       time.time()))).hexdigest()

            data = Host.objects.filter(business=i).order_by("-env")
            pro_count = data.filter(idle=True).count()
            idle_count = data.filter(idle=False).count()
            if idle_count > 0:
                Pro_name = "%s  <span style='color:#1c84c6;'> (%s/%s) </span>" % (i.service_name, pro_count, idle_count)
            else:
                Pro_name = "%s  <span style='color:#1c84c6;'> (%s) </span>" % (i.service_name, pro_count)
            # Pro_name = "<span class='nav-label'>%s </span>  <span class='label label-warning pull-right'> %s </span>" % (i.service_name, pro_count)

            ztree_data.append({"id": str(i.uuid), "pId": tree_uuid, "status": 2, "name": Pro_name, "token": token,
                               "t": i.service_name,
                               "uuid": str(i.uuid), 'pos': True, "open": True,
                               # "icon": "/static/img/zTreeStyle/img/diy/2.png",
                               })

            idle_data = str(hashlib.sha1(i.line_id + "空闲").hexdigest())


            for k in data:
                if not k.idle:
                    env_name = "<span style='color:#d9534f;'>空闲</span>_%s" % k.eth1
                elif k.env:
                    if k.env == "prod":
                        env_name = "<span style='color:#1c84c6;'>%s</span>_%s" % (k.env, k.eth1)
                    if k.env == "st":
                        env_name = "<span style='color:#ec971f;'>%s</span>_%s" % (k.env, k.eth1)
                    if k.env == "pub":
                        env_name = "<span style='color:#5cb85c;'>%s</span>_%s" % (k.env, k.eth1)
                else:
                    env_name = "%s" % k.eth1

                # if k.idle:
                ztree_data.append(
                    {"id": str(k.uuid), "pId": str(i.uuid), "name": env_name, "status": 3, "token": token,
                     "uuid": str(k.uuid), 'pos': True, "open": True,
                     # "icon": "/static/images/ico/linux5.png",
                     "icon": "/static/img/zTreeStyle/img/diy/linux-ico.png",
                     })
                # else:

                if not k.idle:
                    # if idle_data not in idle_list:
                    if idle_data not in idle_list:
                        idle_list.append(idle_data)
                        ztree_data.append(
                                {"id": idle_data, "pId": tree_uuid, "status": 4, "name": "<span style='color:#ed5565;'>空闲</span>", "token": token,
                                 "t": i.service_name,
                                 "uuid": str(i.uuid), 'pos': True, "open": True,
                                 # "icon": "/static/img/zTreeStyle/img/diy/2.png",
                                 })

                    if k.eth1 not in iplist:
                        iplist.append(k.eth1)
                        ztree_data.append(
                            {"id": str(k.uuid), "pId": idle_data, "name": env_name, "status": 3, "token": token,
                             "uuid": str(k.uuid), 'pos': True, "open": True,
                             # "icon": "/static/images/ico/linux5.png",
                             "icon": "/static/img/zTreeStyle/img/diy/linux-ico.png",
                             })

                            # ztree_data.append({{"pId": str(i.uuid), "name": [i[0] for i in ENVIRONMENT]}})

        except AttributeError:
            pass
    return ztree_data
