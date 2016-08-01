#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: server_auth.py
#         Desc: 2014-14/12/19:下午3:11
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from users.models import server_auth
from assets.models import Project, Host
from django.http import HttpResponse, HttpResponseRedirect
from users.models import department_Mode
from users.models import CustomUser
from api.api import uerdel
from accounts.forms import AuthNodeForm
from django import forms
import json
from cmdb_auth.models import AuthNode
from api.api import RabApi


class server_from(forms.ModelForm):
    """
    server_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'服务器')
    user_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'用户名')
    auth_weights = models.CharField(max_length=32, blank=True, null=True, default=u"普通用户", choices=auth_id, verbose_name=u'权限')
    datetime = models.DateTimeField(auto_now=True)

    """

    class Meta:
        model = server_auth
        fields = [
            # "server_ip",
            # "user_name",
            # "auth_weights",
        ]


class business_forms(forms.ModelForm):
    """
    server_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'服务器')
    user_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'用户名')
    auth_weights = models.CharField(max_length=32, blank=True, null=True, default=u"普通用户", choices=auth_id, verbose_name=u'权限')
    datetime = models.DateTimeField(auto_now=True)

    """

    class Meta:
        model = Project
        fields = [
            "service_name"
        ]


@login_required
def user_auth_server(request, uuid):
    """
    不同用户分配不同服务器权限
    server_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'服务器')
    user_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'用户名')
    auth_weights = models.CharField(max_length=32, blank=True, null=True, default=u"普通用户", choices=auth_id, verbose_name=u'权限')
    datetime = models.DateTimeField(auto_now=True)

    """

    if not request.user.is_superuser:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    user_data = CustomUser.objects.get(uuid=str(uuid))
    if request.method == 'POST':
        data = request.POST
        auth_weights = data["auth_weights"]

        for i in data.getlist("node"):
            server = Host.objects.get(uuid=i)
            if user_data.department.desc_gid == 1001:
                data = AuthNode(user_name=user_data, auth=1, project=str(auth_weights), node=server)
            else:
                data = AuthNode(user_name=user_data, auth=0, project=str(auth_weights), node=server)
            data.save()
            if user_data.department.desc_gid == 1001:
                auth = 1
            else:
                auth = 0

            args = {"user": user_data.username, "type": 1, "auth": 0, "node": server.node_name, "ip": server.eth1,
                    "uid": int(3000 + user_data.id), "gid": int(user_data.department.desc_gid),
                    "ssh_key": (user_data.user_key).replace("ssh-rsa ", "")}
            s = RabApi(args=args)
            s.SendMessage()

        if auth_weights == "all":
            server_list = Host.objects.filter(business__isnull=True)
            server_auth_list = server_auth.objects.filter(first_name=user_data.first_name)
            ip_list = []
            ip_auth = {}
            for i in server_auth_list.values():
                ip_list.append(i["server_ip"])
                ip_auth[i["server_ip"]] = i["auth_weights"]
            return render_to_response('assets/auth_type.html', locals(), context_instance=RequestContext(request))

        else:
            business_name = Project.objects.get(pk=auth_weights)
            server_auth_list = server_auth.objects.filter(first_name=user_data.first_name)
            server_list = Host.objects.filter(business=business_name)
            ip_list = []
            data = AuthNode.objects.filter(project=str(business_name.uuid), user_name=user_data)
            for i in data:
                ip_list.append(i.node.uuid)

            return render_to_response('assets/auth_type.html', locals(), context_instance=RequestContext(request))

    data = server_from

    business = Project.objects.all()

    # return HttpResponse(json.dumps({"status": "403", "message": "Authentication failed"}, ensure_ascii=False, indent=4))
    return render_to_response('user/add_auth.html', locals(), context_instance=RequestContext(request))


@login_required
def user_auth_delete(request):
    """
    权限列表删除
    """
    if not request.user.is_superuser:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    auth_id = request.GET.get("auth_id")
    uuid = request.GET.get("uuid")
    node_data = Host.objects.get(pk=uuid)
    user = CustomUser.objects.get(uuid=str(auth_id))
    print auth_id
    print node_data.uuid
    try:
        print uuid, user
        data = AuthNode.objects.get(node=node_data, user_name=user)
        data.node.clean()
        data.user_name.clean()
        data.delete()
        print "delete is ok"
        print node_data.node_name
        print "*" * 100
        print "*" * 100
        print "*" * 100
        print "*" * 100
        args = {"user": user.username,
                "type": 0,
                "node": node_data.node_name,
                "ip": data.node.eth1
                }
        s = RabApi(args=args)
        print s.SendMessage()

        return HttpResponse(json.dumps({"status": "200", "message": "删除成功"}, ensure_ascii=False, indent=4))
    except server_auth.DoesNotExist:
        print "delete is over"
        return HttpResponse(json.dumps({"status": "404", "message": "无此服务器权限"}, ensure_ascii=False, indent=4))


def server_auth_ip(request):
    """
    根据请求ip获取当前服务器ip，查询此ip有那些用户和服务器权限
    :param request:
    :return:
    """
    ip = "192.168.123.16"
    data = server_auth.objects.filter(server_ip=ip)
    content = {}
    for i in data:
        user_data = CustomUser.objects.get(first_name=i.first_name)
        department_name = u"%s" % (user_data.department)

        auth_gid = department_Mode.objects.get(pk=user_data.department_id)

        content[i.user_name] = {"auth": i.auth_weights, "user_uid": user_data.id + 30000,
                                "department": department_name, "gid": auth_gid.desc_gid}
    if len(content):
        return HttpResponse(json.dumps({"status": "200", "message": content}, ensure_ascii=False, indent=4))
    else:
        return HttpResponse(json.dumps({"status": "404", "message": u'还未分配用户'}, ensure_ascii=False, indent=4))


def server_auth_user(request):
    """
    根据请求ip获取当前服务器ip，查询此ip有那些用户和服务器权限
    :param request:
    :return:
    """
    user = request.GET.get("user")
    user_id = CustomUser.objects.get(username=user)
    data = AuthNode.objects.filter(user_name=user_id)
    content = []
    for i in data:
        server_ip = "%s " % (i.node.eth1)
        content.append(server_ip)

    # return HttpResponse(json.dumps({"status": "200", "message": content}, ensure_ascii=False, indent=4))
    return HttpResponse(content)
