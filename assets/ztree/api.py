#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: api.py
#         Desc: 2015-15/4/16:下午5:54
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
from mysite.settings import auth_key
from assets.models import Host, IDC
import hashlib, time
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
# 登录
from users.models import CustomUser
from assets.models import project_swan
from assets.ztree.service import ztree_tag
from django.shortcuts import get_object_or_404
from assets.models import Host, IDC, Service, Line, Project, HostRecord
from cmdb_auth.models import AuthNode


# songxs add
@login_required
def ztree_project(request):
    line_list = Line.objects.filter()
    business = Project.objects.filter(line__isnull=False)
    no_business = Project.objects.filter(line__isnull=True)
    ztree_data = ztree_tag(request.user.username)

    return render_to_response('default/default.html', locals(), context_instance=RequestContext(request))


@login_required
def ztree_business(request):
    """
    树请求验证
    :param request:
    :return:
    """
    business_name = request.GET.get("uuid", False)
    get_token = str(request.GET.get("token", False))
    ztree_data = ztree_tag(request.user.username)

    try:
        sum_token = str(hashlib.sha1(request.user.username + auth_key + business_name +
                                     time.strftime('%Y-%m-%d', time.localtime(time.time()))).hexdigest())
    except TypeError:
        sum_token = False

    if request.GET.get("options") == "host":
        uuid = request.GET.get('uuid', '')
        ip = request.GET.get('ip', '')
        if uuid:
            host = get_object_or_404(Host, uuid=uuid)
        elif ip:
            host = get_object_or_404(Host, eth1=ip)
        host_record = HostRecord.objects.filter(host=host).order_by('-time')
        user_audit = AuthNode.objects.filter(node=host)
        audit_count = user_audit.count()
        return render_to_response('ztree/host_detail.html', locals(), context_instance=RequestContext(request))


    content_status = True
    idle = request.GET.get("idle", False)

    if get_token != sum_token:
        content_status = False
        return render_to_response('ztree/ztree_service.html', locals(), context_instance=RequestContext(request))

    if business_name != u"未分类":
        try:
            bus_data = Project.objects.get(uuid=request.GET.get("uuid"))
            if not idle:
                server_list = Host.objects.filter(business=bus_data, idle=True).order_by("create_time")
            else:
                server_list = Host.objects.filter(business=bus_data, idle=False).order_by("create_time")
        except:
            pass

    else:
        bus_data = u'未分类'
        idc_data = IDC.objects.filter(type=1)
        if not idle:
            server_list = Host.objects.filter(business__isnull=True, idc=idc_data, idle=True).order_by("create_time")
        else:
            server_list = Host.objects.filter(business__isnull=True, idc=idc_data, idle=False).order_by("create_time")

    if request.GET.get("options") == "swan_push":
        s = Ztree_class(business_name, request.user.first_name)
        rst = s.swan()
        rst_data = rst.get("swan_name")
        status = len(rst_data)
        return render_to_response('ztree/swan.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "doc":
        data = Project.objects.get(pk=business_name)
        # return render_to_response('ztree/swan.html', locals(), context_instance=RequestContext(request))
        return render_to_response('markdown/index.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "highstate":
        project = Project.objects.get(uuid=business_name)
        host_list = Host.objects.filter(business=project)
        return render_to_response('ztree/highstate.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "monitor":
        return render_to_response('ztree/zabbix_count.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "salt":
        return render_to_response('ztree/saltstack.html', locals(), context_instance=RequestContext(request))


    if request.GET.get("options") == "project":
        ip_list = []
        server_list = {}
        line_name = Line.objects.get(pk=business_name)
        business_data = Project.objects.filter(line=business_name)

        for i in business_data:
            node = Host.objects.filter(business=i, idle=True)
            for k in node:
                if k.eth1 not in ip_list:
                    ip_list.append(k.eth1)
                    server_list[str(k.uuid)] = k.eth1
        count = len(ip_list)
        return render_to_response('ztree/project.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "types":
        get_env = request.GET.get("name")
        business_data = Project.objects.filter(pk=business_name)
        server_list = Host.objects.filter(business=business_data, env=get_env).order_by("-create_time")

        count = server_list.count()
        return render_to_response('ztree/ztree.html', locals(), context_instance=RequestContext(request))

    if request.GET.get("options") == "service":
        s = []
        bus_data = Project.objects.get(uuid=business_name)
        server_list = Host.objects.filter(business=bus_data, idle=True).order_by("create_time")

        for i in server_list:
            t = i.service.all()
            for b in t:
                if b not in s:
                    s.append(b)

        tag = request.GET.get("tgt", False)

        if tag:
            service_all = Service.objects.get(name=tag)
            server_list = Host.objects.filter(service=service_all, business=bus_data)

        return render_to_response('ztree/ztree_service.html', locals(), context_instance=RequestContext(request))

    count = server_list.count()
    return render_to_response('ztree/ztree.html', locals(), context_instance=RequestContext(request))


@login_required
def CdnCache(request):
    """
    树请求验证
    :param request:
    :return:
    """
    service = request.GET.get("services")
    get_token = str(request.GET.get("token"))
    uuid = str(request.GET.get("uuid"))

    sum_token = str(hashlib.sha1(request.user.username + auth_key + service + time.strftime('%Y-%m-%d', time.localtime(
            time.time()))).hexdigest())

    content_status = True
    if get_token != sum_token:
        content_status = False

    idc_data = IDC.objects.get(uuid=uuid)
    service_all = Service.objects.get(name=service)
    server_list = Host.objects.filter(idc=idc_data, service=service_all)
    business_name = idc_data.name
    service_tag = service

    return render_to_response('ztree/service.html', locals(), context_instance=RequestContext(request))


@login_required
def CdnIdc(request):
    """
    树请求验证
    :param request:
    :return:
    """
    get_token = str(request.GET.get("token"))
    uuid = str(request.GET.get("uuid"))
    idc_data = IDC.objects.get(uuid=uuid)

    sum_token = str(hashlib.sha1(request.user.username + auth_key + idc_data.name + time.strftime('%Y-%m-%d',
                                                                                                  time.localtime(
                                                                                                          time.time()))).hexdigest())

    content_status = True
    if get_token != sum_token:
        content_status = False

    server_list = Host.objects.filter(idc=idc_data)
    business_name = idc_data.name

    return render_to_response('ztree/idc.html', locals(), context_instance=RequestContext(request))


class Ztree_class(object):
    """
    ztree 类
    """

    def __init__(self, project_name, user):
        self.project_name = project_name
        self.user = user

    def monitor(self):
        return True

    def swan(self):
        rst_data = {}

        user_info = CustomUser.objects.get(first_name=self.user)

        myform_rst = Project.objects.get(uuid=self.project_name)

        rst = project_swan.objects.filter(project_name_id=myform_rst.uuid)

        """
        所有当前项目发布名称放到一个list中
        """

        swan_name_list = [i.swan_name for i in rst]
        swan_push = user_info.project_swan_set.all()
        user = CustomUser.objects.get(first_name=self.user)

        if user.is_superuser:

            for i in rst:
                rst_data[str(i.uuid)] = i.swan_name

        else:
            swan_push = user_info.project_swan_set.all()
            for i in swan_push:
                if i.swan_name in swan_name_list:
                    rst_data[str(i.uuid)] = i.swan_name

        host_list = myform_rst.host_set.all()
        content = {"swan_name": rst_data, "host": host_list}

        return content

    def highstate(self):
        project = Project.objects.get(service_name=self.project_name)
        # server_list = project.host_set
        host_list = Host.objects.filter(business=project)

        return True


@csrf_exempt
def ZtreeIndex(request):
    """

    :param request:
    :return:
    """
    if request.method == 'POST':
        otherParam = request.POST.get("otherParam")
        status = request.POST.get("status")
        line_id = request.POST.get("line_id")

        try:
            name = request.POST.get("name")
            id = request.POST.get("id")

        except:
            name = False

        if not name:
            ztree = ztree_tag(request.user.username)
            return HttpResponse(json.dumps(ztree, ensure_ascii=False, indent=4))

        elif int(status[0]) == 1:
            ztree = []
            return HttpResponse(json.dumps(ztree, ensure_ascii=False, indent=4))

        else:
            ztree = []
            bus_data = Project.objects.get(service_name=name)
            server_list = Host.objects.filter(business=bus_data).order_by("create_time")

            s = []
            for i in server_list:
                t = i.service.all().values()
                for b in t:
                    if b not in s:
                        s.append(b)
            tree_id = 0
            for i in s:
                tree_id += 1

                token = hashlib.sha1(request.user.username + auth_key + i.get("name") + time.strftime('%Y-%m-%d',
                                                                                                      time.localtime(
                                                                                                              time.time()))).hexdigest()

                ztree.append({"id": tree_id, "status": 3, "line_id": line_id, "name": i.get("name"), "token": token,
                              "t": i.get("name"), "business": bus_data.service_name})

            return HttpResponse(json.dumps(ztree, ensure_ascii=False, indent=4))
    content = {"status": 403, "message": "auth error"}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))
