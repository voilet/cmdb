#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 
#      History:
# =============================================================================

from django.http import HttpResponse, HttpResponseRedirect
from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch, Project
from users.models import CustomUser
from mysite.settings import salt_api_pass, salt_api_user, salt_api_url, pxe_url_api, auth_content, app_key, app_name, \
    auth_url, auth_key, springboard
import json
import hashlib
from django.views.decorators.csrf import csrf_exempt
from django import forms
from cmdb_auth.models import AuthNode


# 按服务排序
# @auth_login_required
# @csrf_protect
def type_list_id(request, id):
    """
    按项目id查相关项目的用户信息
    """
    content = {}
    business_name = Project.objects.get(id=id)
    content["name"] = business_name.service_name
    content["aliases_name"] = business_name.aliases_name
    content['user'] = {}
    content['node'] = []
    server_list = business_name.host_set.all()
    for node in server_list:
        content['node'].append(node.node_name)
    server_user_all = business_name.service_user.all()
    for i in server_user_all:
        content['user'][i.username] = {'mobile': i.mobile, 'email': i.email, "user_key": i.user_key}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


def type_list(request):
    content = {}
    business_name = Project.objects.all()
    for i in business_name:
        content[i.service_name] = {'id': i.id, 'description': i.description}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


def user_select(request):
    """
    用户接口，跳板机请求返回用户权限列表
    """
    content = {"status": "200", "message": {}}
    search = request.GET.get("ip", False)
    username = request.GET.get("username", False)

    if not search:
        try:
            user_list = CustomUser.objects.get(username=username)
            data = AuthNode.objects.filter(user_name=user_list)
            for i in data:
                proj = Project.objects.get(uuid=str(i.project))
                content["message"][i.node.eth1] = proj.service_name
            return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))
        except CustomUser.DoesNotExist:
            return HttpResponse(json.dumps({"status": "403", "message": u"无此权限"}, ensure_ascii=False, indent=4))
    else:
        try:
            user_list = CustomUser.objects.get(username=username)
            ip = Host.objects.get(eth1=search)
            data = AuthNode.objects.filter(user_name=user_list, node=ip).count()
            if data > 0:
                return HttpResponse(json.dumps({"status": "200", "message": u"有此机器权限"}, ensure_ascii=False, indent=4))
        except CustomUser.DoesNotExist:
            pass

    return HttpResponse(json.dumps({"status": "403", "message": u"无此权限"}, ensure_ascii=False, indent=4))


def user_class(request):
    """
    根据项目查当前项目下用户，生成相应saltstack加用户配置文件
    """
    content = {}
    business_name = Project.objects.all()
    for prod_name in business_name:
        user_list = []
        # print i.service_name
        prod_id = prod_name.id
        business_name = Project.objects.get(id=prod_id)
        test = prod_name.service_name
        content[test] = prod_name.service_name
        # print type(prod_name.service_name)
        # content[prod_name.service_name]["user"] = 123
        # content['user'] = {}
        # content['node'] = []
        server_list = business_name.host_set.all()
        # for node in server_list:
        #     content['node'].append(node.node_name)
        server_user_all = business_name.service_user.all()
        for i in server_user_all:
            user_list.append({'username': i.username, "user_key": i.user_key})

        # content[i.service_name] = {'id': i.id, 'description': i.description}
        content[test] = user_list
        # content[test]["user"] = user_list
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))


def saltstack_create_config(request):
    content = {}
    business_name = Project.objects.all()
    for i in business_name:
        content[i.service_name] = {}
        api_id = i.id
        business_name = Project.objects.get(id=api_id)
        # content[i.service_name]["name"] = business_name.service_name
        content[i.service_name]['user'] = {}
        content[i.service_name]['node'] = []
        server_list = business_name.host_set.all()
        for node in server_list:
            content[i.service_name]['node'].append(node.node_name)
        server_user_all = business_name.service_user.all()
        for user in server_user_all:
            content[i.service_name]['user'][user.username] = {"user_key": user.user_key, "user_id": user.id,
                                                              "department": user.department}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


@csrf_exempt
def Sn_number(request):
    """
    sn编号查询，返回记录IP
    """
    if request.method == 'POST':
        sn = request.POST.get("sn", False)
        mac = request.POST.get("mac", False)
        if sn and len(sn) > 0:
            try:
                ip = Host.objects.get(server_sn=sn)
                return HttpResponse(u"%s\n" % ip.eth1)
            except:
                pass
        if mac and len(mac) > 0:
            try:
                ip = Host.objects.get(mac=str(mac).replace(':', '-').strip(" "))
                return HttpResponse(u"%s\n" % ip.eth1)
            except:
                pass
    return HttpResponse(u"%s\n" % "169.186.1.1")


def CmdbUpdate(request):
    """
    sn编号查询，返回记录IP
    """
    import requests
    url = "http://192.168.8.80:8000/cmdb/"
    s = requests.get(url)
    rst = s.json()
    data = rst.get("result")
    idc = IDC.objects.get(pk="9b70bec5660441c2ae10908da1db38d3")
    for i in data:
        result = i.get("fields")
        try:
            host_data = Host.objects.get(eth1=result.get("eth1"))
            host_data.cpu = result.get("cpu", "")
            host_data.memory = result.get("memory", "")
            host_data.hard_disk = result.get("hard_disk", "")
            host_data.brand = result.get("brand", "Dell R410")
            host_data.editor = result.get("editor", "")
            host_data.number = result.get("number", "")
            host_data.eth2 = result.get("eth2", "")
            host_data.save()
        except:
            cmdb = Host(node_name=result.get("node_name"),
                        eth1=result.get("eth1"),
                        mac=result.get("mac"),
                        internal_ip=result.get("internal_ip"),
                        brand=result.get("brand"),
                        cpu=result.get("cpu"),
                        idc=idc,
                        system="CentOS",
                        system_cpuarch="X86_64",
                        cabinet=result.get("cabinet"),
                        server_cabinet_id=result.get("server_cabinet_id"),
                        number=result.get("number"),
                        editor=result.get("editor"),
                        status=result.get("status", 1),
                        room_number=result.get("room_number"),
                        hard_disk=result.get("hard_disk"),
                        eth2=result.get("eth2", ""),
                        memory=result.get("memory", ""),
                        server_sn=result.get("server_sn", ""))
            cmdb.save()
    return HttpResponse(json.dumps({"status": 403, "result": u"参数不正确"}, ensure_ascii=False, indent=4, ))
