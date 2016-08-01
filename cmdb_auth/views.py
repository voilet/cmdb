#!/usr/bin/python
# -*-coding:utf-8-*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from users.models import CustomUser
from django.contrib.sessions.backends.db import SessionStore, Session
import json
from accounts.auth_session import auth_class
from forms import cmdb_from, auth_add, auth_add_user, auth_add_swan_user
from cmdb_auth.models import auth_group, user_auth_cmdb
from assets.models import project_swan, Host, Project, Line
from accounts.user_mode.server_auth import server_from
from cmdb_auth.models import AuthNode
from assets.ztree.service import ztree_tag
from assets.models import Host, IDC
import hashlib, time
from mysite.settings import auth_key
from assets.models import Line, Service
from api.api import RabApi
from users.models import server_auth


@login_required
def cmdb_auth(request):
    data = cmdb_from()
    if request.method == 'POST':
        uf = cmdb_from(request.POST)
        if uf.is_valid():
            uf.save()

            return HttpResponseRedirect("/auth/cmdb/")
        return render_to_response('auth/cmdb.html', locals(), context_instance=RequestContext(request))
    else:

        return render_to_response('auth/cmdb.html', locals(), context_instance=RequestContext(request))


@login_required
def auth_index(request):
    u"""
    权限首页
    :param request:
    :return:
    """
    data = auth_group.objects.all().order_by("-date_time")
    group_user_count = {}

    for i in data:
        data_id = auth_group.objects.get(uuid=i.uuid)
        group_user_count[i.uuid] = data_id.group_user.all().count()

    return render_to_response('auth/index.html', locals(), context_instance=RequestContext(request))


def auth_session_clsss(uuid):
    """

    :return:
    """
    data_id = auth_group.objects.get(uuid=uuid)
    all_user = data_id.group_user.all()
    for i in all_user:
        if i.session_key:
            s = SessionStore(session_key=i.session_key)
            s["fun_auth"] = auth_class(i)
            s.save()

    return True


@login_required
def add_auth(request, uuid):
    """
    add auth
    :param request:
    :return:
    """
    uuid = str(uuid)
    group_uuid = auth_group.objects.get(uuid=uuid)

    try:
        group_data = user_auth_cmdb.objects.get(group_name=uuid)
        data = auth_add(instance=group_data)
    except:
        data = auth_add()

    if request.method == 'POST':
        try:
            uf = auth_add(request.POST, instance=group_data)
        except:
            uf = uf = auth_add(request.POST)

        if uf.is_valid():
            uf.save()

            auth_session_clsss(uuid)

    return render_to_response('auth/add_auth.html', locals(), context_instance=RequestContext(request))


@login_required
def delete_auth(request, uuid):
    """
    add auth
    :param request:
    :return:
    """
    uuid = str(uuid)
    group_uuid = auth_group.objects.get(uuid=uuid)
    group_uuid.group_user.clear()
    group_uuid.delete()

    return HttpResponseRedirect('/auth/cmdb/')


def add_group_user(request, uuid):
    """
    :param requests:
    :param uuid:
    :return:
    """
    uuid = str(uuid)
    data_id = auth_group.objects.get(uuid=uuid)

    if request.method == 'POST':
        uf = auth_add_user(request.POST, instance=data_id)
        if uf.is_valid():
            uf.save()
            auth_session_clsss(uuid)

    data = auth_add_user(instance=data_id)
    userall = CustomUser.objects.all()
    all_user = data_id.group_user.all()

    user_list = [x.first_name for x in all_user]

    return render_to_response('auth/group_user.html', locals(), context_instance=RequestContext(request))


@login_required
def edit_auth(request, uuid):
    """
    add auth
    :param request:
    :return:
    """
    uuid = str(uuid)
    group_uuid = auth_group.objects.get(uuid=uuid)
    if request.method == 'POST':
        uf = cmdb_from(request.POST, instance=group_uuid)
        if uf.is_valid():
            uf.save()
            return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4, ))

    else:
        data = cmdb_from(instance=group_uuid)

    return render_to_response('auth/jquery_from.html', locals(), context_instance=RequestContext(request))


@login_required
def edit_status(request, uuid):
    """
    add auth
    :param request:
    :return:
    """
    uuid = str(uuid)
    group_uuid = auth_group.objects.get(uuid=uuid)
    if group_uuid.enable:
        group_uuid.enable = False
        group_uuid.save()
        auth_session_clsss(uuid)
    else:
        group_uuid.enable = True
        group_uuid.save()
        auth_session_clsss(uuid)

    return HttpResponse(json.dumps({"status": 200, "msg": "ok"}, ensure_ascii=False, indent=4, ))


@login_required
def auth_swan(request):
    u"""
    权限首页
    :param request:
    :return:
    """
    data = project_swan.objects.all()
    return render_to_response('auth/swan_index.html', locals(), context_instance=RequestContext(request))


@login_required
def auth_swan_user(request, uuid):
    u"""
    权限首页
    :param request:
    :return:
    """
    data = project_swan.objects.get(pk=uuid)
    if request.method == 'POST':
        uf = auth_add_swan_user(request.POST, instance=data)

        if uf.is_valid():
            uf.save()

    userall = CustomUser.objects.all()
    all_user = data.push_user.all()
    user_list = [x.first_name for x in all_user]

    return render_to_response('auth/swan_user.html', locals(), context_instance=RequestContext(request))


@login_required
def user_select(request):
    u"""
    服务器权限管理
    """
    uf = CustomUser.objects.all()
    return render_to_response('auth/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def ztree_business(request):
    u"""
    树请求验证
    :param request:
    :return:
    """
    business_name = request.GET.get("name")
    get_token = str(request.GET.get("token"))
    user = request.GET.get("user")
    sum_token = str(hashlib.sha1(request.user.username + auth_key + business_name + time.strftime('%Y-%m-%d',
                                                                                                  time.localtime(
                                                                                                      time.time()))).hexdigest())
    userId = str(user)
    user_data = CustomUser.objects.get(uuid=userId)

    if get_token != sum_token:
        content_status = False

    if request.method == 'POST':
        data = request.POST
        auth_weights = data.get("auth_weights", False)
        auth = int(data.get("auth"))
        for i in data.getlist("node_name"):
            server = Host.objects.get(uuid=i)
            # if user_data.department.desc_gid == 1001:
            if AuthNode.objects.filter(user_name=user_data, node=server).count() == 0:
                data = AuthNode(user_name=user_data, auth=auth, node=server)
                data.save()

                args = {"user": user_data.username,
                        "type": 1,
                        "auth": auth,
                        "node": server.node_name,
                        "ip": server.eth1,
                        "uid": int(3000 + user_data.id),
                        "gid": int(user_data.department.desc_gid),
                        "ssh_key": (user_data.user_key).replace("ssh-rsa ", "")}
                print args
                s = RabApi(args=args)
                print s.SendMessage()
            else:
                print u"数据已存在"

    data = server_from()
    business = Project.objects.all()
    all_node = AuthNode.objects.filter(user_name=user_data)
    ip_list = [i.node.eth1 for i in all_node]
    node_count = all_node.count()

    if business_name != u"未分类":
        bus_data = Project.objects.get(pk=request.GET.get("name"))
        server_list = Host.objects.filter(business=bus_data).order_by("create_time")

    else:
        bus_data = u'未分类'
        idc_data = IDC.objects.filter(type=1)
        server_list = Host.objects.filter(business__isnull=True, idc=idc_data).order_by("create_time")

    ztree_data = ztree_tag(request.user.username)

    content_status = True

    return render_to_response('auth/add_host_auth_project.html', locals(), context_instance=RequestContext(request))


@login_required
def user_count(request, uuid):
    u"""
    服务器权限管理
    """
    user = CustomUser.objects.get(uuid=uuid)
    data = AuthNode.objects.filter(user_name=user)
    return render_to_response('auth/node_list.html', locals(), context_instance=RequestContext(request))


@login_required
def user_auth_server(request, uuid):
    u"""
    不同用户分配不同服务器权限

    """
    userId = str(uuid)
    user_data = CustomUser.objects.get(uuid=uuid)
    data = server_from()
    business = Project.objects.all()
    all_node = AuthNode.objects.filter(user_name=user_data)
    node_count = all_node.count()

    line_list = Line.objects.filter()
    business = Project.objects.filter(line__isnull=False)
    no_business = Project.objects.filter(line__isnull=True)
    ztree_data = ztree_tag(request.user.username)
    users = 108
    hosts = Host.objects.all()
    problems = 20

    return render_to_response('auth/add_host_auth_ztree.html', locals(), context_instance=RequestContext(request))
