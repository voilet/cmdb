#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
#=============================================================================

import json, time, urllib
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from assets.models import Host, IDC, System_os, system_arch, ENVIRONMENT, room_hours, Line, Project, Service
from assets.models import Project, System_usage
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from users.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from salt_ui.api.salt_token_id import *
from cmdb_auth.no_auth import check_auth
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from assets.forms import HostForm


import requests, re
from users.models import server_auth
from assets.new_api import pages
from assets.models import SERVER_STATUS, Server_System


@login_required
def host_without_business(request):


    hosts = Host.objects.all().order_by("-eth1")
    node_list = hosts.filter(business__isnull=True)

    idcs = IDC.objects.filter()
    lines = Line.objects.all()
    server_type = Project.objects.all()
    services = Service.objects.all()
    brands = Server_System
    server_status = SERVER_STATUS
    server_list_count = hosts.count()
    physics = Host.objects.filter(vm__isnull=True).count()
    vms = Host.objects.filter(vm__isnull=False).count()

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(node_list, request)
    return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))


@login_required
def auth_host_without_business(request):

    server_list = Host.objects.filter(business__isnull=True)
    auth_id = request.GET.get("auth_id")
    user_data = CustomUser.objects.get(pk=auth_id)
    server_auth_list = server_auth.objects.filter(first_name=user_data.first_name)
    ip_list = []
    ip_auth = {}
    for i in server_auth_list.values():
        ip_list.append(i["server_ip"])
        ip_auth[i["server_ip"]] = i["auth_weights"]

    return render_to_response('assets/auth_type.html', locals(), context_instance=RequestContext(request))

# @login_required
def restart_node(reques, uuid):
    """
    机器重置是将status置为0，即可重新初始化系统
    """

    restart_id = Host.objects.get(uuid=str(uuid))
    restart_id.status = 0
    restart_id.save()
    return HttpResponseRedirect('/salt/install/')
    # return HttpResponse("is ok")

# class Host_from(forms.ModelForm):
#
#     # FAVORITE_COLORS_CHOICES = Project.objects.values_list("id", "service_name")
#     # business = forms.MultipleChoiceField(required=False,
#     #     widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES, label=u"项目")
#
#     class Meta:
#         model = Host
#         fields = ["node_name", "idc", "room_number", "eth1", "eth2", "mac", "internal_ip", "room_number", "cabinet",
#                  "server_cabinet_id", "number", "business", "service", "env",
#                   "cpu", "core_num", "hard_disk", "memory", "system", "system_cpuarch", "sort", "vm", "Services_Code",
#                   "brand", "guarantee_date", "server_sn", "editor"]

# class vm_from(forms.ModelForm):
#
#     class Meta:
#         model = Host
#         fields = ["node_name", "cabinet", "number", "business", "env",
#                   "cpu", "core_num", "hard_disk", "memory", "system", "system_cpuarch", "sort", "vm",
#                   "brand"]

class server_room_hous(forms.ModelForm):

    class Meta:
        model = Host
        fields = ["room_number", "cabinet"]

def verifyDomainNameFormart(hostname, idc):
    """
    验证主机名是否合法
    """
    # allow_idc = '(' + "|".join(idc) + ')'
    # allow_product_line = '(' + "|".join(Environment) + ')'
    # regex = """(^(l|i)-){0,1}(n-[a-z0-9]+|[a-z0-9]{1,20}\.[a-z0-9]{1,20}\.%(allow_product_line)s)\.(%(allow_idc)s)$""" % \
    #         {'allow_product_line': allow_product_line, 'allow_idc': allow_idc}
    # m = re.match(regex, hostname)
    # if m:
    #     return True
    return True


def MAC_formart(mac):
    """
    验证MAC是否合法
    """
    regex = """(^([0-9A-Fa-f]{2})(-[0-9A-Fa-f]{2}){5}|([0-9A-Fa-f]{2})(:[0-9A-Fa-f]{2}){5}$)"""
    m = re.match(regex, mac)
    if m and Host.objects.filter(mac=mac).count() == 0:
        return True
    return False


# @login_required
# @csrf_protect
# def node_add(request):
#     """
#     添加资产方法
#     """
#     status = check_auth(request, "add_host")
#     if not status:
#         return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))
#
#     content = {}
#     server_type = Project.objects.all()
#     idc_name = IDC.objects.all()
#     idc_list = [i.name for i in idc_name]
#     env = Environment
#
#     
#     if request.method == 'POST':
#         uf = Host_from(request.POST)
#         
#         if uf.is_valid():
#             # uf.save()
#             #如果commit为False,则ManyToMany就需要使用以下方法
#             zw = uf.save(commit=False)
#             zw.edit_username = request.user.username
#             zw.mac = str(request.POST.getlist("mac")[0]).replace(':', '-').strip(" ")
#             zw.status = 0
#             zw.vm = 0
#             zw.save()
#             uf.save_m2m()
#             return HttpResponseRedirect('/assets/server/')
#     else:
#         uf = Host_from()
#         business = Project.objects.all()






@login_required
@csrf_protect
def update_cabinet(request):
    if request.method == 'POST':
        node_name = request.POST.get('node_name', '')
        cabinet = request.POST.get('cabinet', '')
        room_number = request.POST.getlist('room_number')
        if not cabinet:
            data = {'status': False, 'msg': u"请填写机柜位置"}
            return HttpResponse(json.dumps(data))

        node_name_list = node_name.split(',')
        node_list = []
        for name in node_name_list:
            try:
                node = Host.objects.get(node_name=name)
            except:
                msg = u"%s主机错误" % name
                data = {'status': False, 'msg': msg}

                return HttpResponse(json.dumps(data))
            node_list.append(node)
        for node in node_list:
            node.cabinet = cabinet
            node.room_number = room_number[0]
            node.save()

        data = {'status': True, 'msg': 'success'}
        return HttpResponse(json.dumps(data))

    else:
        node_name = request.GET.get('node_name', '')
        uf = server_room_hous()
        return render_to_response('assets/update_cabinet.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def update_system(request):
    if request.method == 'POST':
        is_success = True
        node_name = request.POST.get('node_name', '')
        system = request.POST.get('system', '')
        if not system or system not in zip(*System_os)[0]:
            is_success = False
        system_cpuarch = request.POST.get('system_cpuarch', '')
        if not system_cpuarch or system_cpuarch not in zip(*system_arch)[0]:
            is_success = False
        sort = request.POST.get('sort', '')
        if not sort or sort not in zip(*System_usage)[0]:
            is_success = False
        if not is_success:
            data = {'status': False, 'msg': u"数据选择错误"}
            return HttpResponse(json.dumps(data))

        node_name_list = node_name.split(',')
        node_list = []
        for name in node_name_list:
            try:
                node = Host.objects.get(node_name=name)
            except:
                msg = u"%s主机错误" % name
                data = {'status': False, 'msg': msg}
                return HttpResponse(json.dumps(data))
            node_list.append(node)
        for node in node_list:
            node.system = system
            node.system_cpuarch = system_cpuarch
            node.sort = sort
            node.save()
        data = {'status': True, 'msg': 'success'}
        return HttpResponse(json.dumps(data))

    else:
        node_name = request.GET.get('node_name', '')
        system_os = System_os
        system_cpuarch = system_arch
        system_usage = System_usage
        return render_to_response('assets/update_system.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def select_business(request):
    if request.method == 'POST':
        node_name = request.POST.get('node_name', '')
        business_id = request.POST.get('business', '')
        env = request.POST.get('env', '')
        if not env or env not in zip(*ENVIRONMENT)[0]:
            data = {'status': False, 'msg': u"环境选择错误"}
            return HttpResponse(json.dumps(data))
        if not business_id:
            business = None
        else:
            business = get_object_or_404(Project, pk=business_id)

        node_name_list = node_name.split(',')
        node_list = []
        for name in node_name_list:
            try:
                node = Host.objects.get(node_name=name)
            except:
                msg = u"%s主机错误" % name
                data = {'status': False, 'msg': msg}
                return HttpResponse(json.dumps(data))
            node_list.append(node.node_name)
        business_id = Project.objects.get(pk=business_id)
        for node in node_list:
            node = Host.objects.get(node_name=node)
            # 添加到新增项目中
            business_id.host_set.add(node)

            s = business_id.save()
            if s:
                node.env = env
            else:
                node.env = ''
            node.save()
        data = {'status': True, 'msg': 'success'}
        return HttpResponse(json.dumps(data))

    else:
        env_list = ENVIRONMENT
        business_list = Project.objects.all()
        node_name = request.GET.get('node_name', '')
        return render_to_response('assets/select_business.html', locals(), context_instance=RequestContext(request))



@login_required
@csrf_protect
def Index_add_batch(request):
    '''
    批量添加资产
    '''

    status = check_auth(request, "bat_add_host")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    content = {}
    batch_error = []
    batch_ok = []
    test = {}
    server_type = Project.objects.all()
    content["server_type"] = server_type
    idc_name = IDC.objects.all()
    idc_list = [i.name for i in idc_name]
    if request.method == 'POST':    
        uf = request.POST["add_batch"]
        for i in uf.split("\r\n"):
            i = i.split()
            if len(i) == 6:
                #判断主机名
                node_name = i[0]
                #检测主机名是否合法
                mac = str(i[1]).replace(':', '-')

                if not verifyDomainNameFormart(node_name, idc_list) \
                    or not MAC_formart(mac) \
                    or i[2] not in ["default", "openstack"] \
                    or i[4] not in ["CentOS", "Debian"] \
                    or i[3] not in ["DELL", "HP", "Other"] \
                    or i[5] not in ["x86_64", "i386", "X86_64"]:
                    error_return = "{nodename}:{name_return}  {MAC}:{mac_return}  {System_usage}:{System_usage_return}  {system}:{system_return}  {brand}:{brand_return}  {system_cpuarch}:{system_cpuarch_return}" \
                        .format(
                                  nodename=i[0], name_return=verifyDomainNameFormart(node_name, idc_list),
                                  # eth1=i[1],
                                  System_usage=i[2], System_usage_return=i[2] in ["default", "openstack", "cloud"],
                                  system=i[4], system_return=i[4] in ["CentOS", "Debian"],
                                  brand=i[3], brand_return=i[3] in ["DELL", "HP", "Other"],
                                  system_cpuarch=i[5], system_cpuarch_return=i[5] in ["x86_64", "i386", "X86_64"]
                    )
                    # test[i[0]] = {i[0]: verifyDomainNameFormart(node_name, idc_list), i[1]: MAC_formart(mac), i[2]: i[2] in ["default", "openstack"], i[4]: i[4] in ["CentOS", "Debian"], i[3]: i[3] in ["DELL", "HP", "Other"], i[5]: i[5] in ["x86_64", "i386"]}
                    print error_return
                    batch_error.append(error_return)
                else:
                    batch_ok.append(i)
            else:
                batch_error.append(i)
        for i in batch_ok:
            print i[0], str(i[1]).replace(':', '-'), i[2], i[3], i[4], i[5]
            mac = str(i[1]).replace(':', '-')
            host = Host(node_name=i[0], eth1=i[1], sort=i[2], brand=i[3], system=i[4], system_cpuarch=i[5])
            host.save()
        # print batch_error
        content["error"] = batch_error
        content["batch"] = False
        content.update(csrf(request))
        return render_to_response('assets/add_batch.html', content, context_instance=RequestContext(request))
    else:
        content.update(csrf(request))
        content["batch"] = True
        return render_to_response('assets/add_batch.html', content, context_instance=RequestContext(request))


@login_required
@csrf_protect
def services_list_id(request, uuid):
    """
    fancybox 数据 popup
    """
    node = Host.objects.get(pk=uuid)
    return render_to_response('assets/ajax_item.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def services_room_id(request):
    """
    服务器位置保存
    :param requests:
    :return:
    """
    if request.method == 'POST':
        service_list = request.POST.get("list1SortOrder").split("|")

        s = 0
        for i in service_list:
            s += 1
            service_data = Host.objects.get(eth1=i)
            service_data.cabinet = s
            service_data.save()

        return render_to_response('assets/ajax_item.html', locals(), context_instance=RequestContext(request,))

# @login_required
# @csrf_protect
def server_edit(request, uuid):
    """
    修改主机
    """
    content = {}
    edit_id = Host.objects.get(uuid=uuid)
    test_name = edit_id.node_name
    old_ip = edit_id.eth1
    idc_name = IDC.objects.all()
    server_type = Project.objects.all()
    uf = HostForm(instance=edit_id)
    if request.method == 'POST':    
        uf = HostForm(request.POST, instance=edit_id)   
        if uf.is_valid(): 
            zw = uf.save(commit=False)
            zw.edit_username = request.user.username
            zw.mac = str(request.POST.getlist("mac")[0]).replace(':', '-').strip(" ")
            zw.save()
            uf.save_m2m()
            user_all = request.user
            # idc_log(user_all.username, edit_id.node_name, "修改", edit_id.edit_username, edit_id.edit_datetime, id, user_all.id)
            return HttpResponse(json.dumps({"status": "ok"}, ensure_ascii=False, indent=4,))

    else:
        uf = HostForm(instance=edit_id)
        business = Project.objects.all()
        business_group = edit_id.business.all()

        return render_to_response('assets/host_edit.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def Node_search(request):
    """
    根据主机搜索
    """
    status = check_auth(request, "select_host")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    content = {}
    os = System_os
    number = room_hours
    idcs = IDC.objects.filter()
    # if request.method == 'GET':
    try:
        search_name = request.GET.get("host_node")
        # search_name = search_name[0]
        server_list = Host.objects.filter(node_name__contains=search_name)
        server_list_count = server_list.count()

        content["search_return"] = False
        eth = False

        if server_list_count > 0:
            content["search_return"] = True

        elif not content["search_return"]:
            server_list = Host.objects.filter(eth1__contains=search_name)
            server_list_count = server_list.count()
            if server_list_count == 0:
                server_list = Host.objects.filter(cabinet=search_name)
                server_list_count = server_list.count()

                server_cloud_count = Host.objects.filter(cabinet=search_name, sort="cloud").count()
                centos = Host.objects.filter(cabinet__contains=search_name, system="CentOS").count()
                server_node = server_list_count - server_cloud_count

                content["search_return"] = True

        else:
            content["search_return"] = False
        business_list = []
        for i in server_list:
            business_list.append({i.eth1: i.business.all()})

        return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))
    except:

        # return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))
        return HttpResponseRedirect('/assets/server/')


@login_required
@csrf_protect
def search_cabinet(request):
    """
    根据主机搜索
    """
    content = {}
    os = System_os
    number = room_hours
    idcs = IDC.objects.filter()
    cabinet = request.GET.get("cabinet")
    room_number = request.GET.get("room_number")
    if len(room_number):
        server_list = Host.objects.filter(cabinet=cabinet, room_number=room_number)
        server_cloud_count = Host.objects.filter(cabinet=cabinet, room_number=room_number, sort="cloud").count()
        centos = Host.objects.filter(cabinet=cabinet, room_number=room_number, system="CentOS").count()
    else:
        server_list = Host.objects.filter(cabinet=cabinet)
        server_cloud_count = Host.objects.filter(cabinet=cabinet, sort="cloud").count()
        centos = Host.objects.filter(cabinet=cabinet, system="CentOS").count()
    os = System_os
    idcs = IDC.objects.filter()
    server_type = Project.objects.all()
    server_list_count = server_list.count()
    server_node = server_list_count - server_cloud_count

    business_list = []
    for i in server_list:
        business_list.append({i.eth1: i.business.all()})

    return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))


@login_required
def select_default(request):
    """
     根据主机搜索
    """
    content = {}
    os = System_os
    number = room_hours
    idcs = IDC.objects.filter()

    search_name = request.GET['name']
    if search_name == "cloud":
        node_list = Host.objects.filter(sort__contains="cloud")
        server_list_count = node_list.count()
        centos = Host.objects.filter(sort__contains="cloud", system="CentOS").count()
        debian = server_list_count - centos
        server_cloud_count = server_list_count

        return render_to_response('assets/search.html', locals(), context_instance=RequestContext(request))
    else:
        node_list = Host.objects.all().exclude(sort__contains="cloud")
        server_list_count = node_list.count()
        centos = Host.objects.all().exclude(sort__contains="cloud").filter(system="CentOS").count()
        debian = server_list_count - centos
        server_node = server_list_count
        server_cloud_count = 0

        return render_to_response('assets/search.html', locals(), context_instance=RequestContext(request))


@login_required
def Node_select(request):
    """
     根据主机搜索
    """


    content = {}
    if request.method == 'POST':
        search_name = request.POST["node_name"]
        node = Host.objects.filter(node_name=search_name).count()
        if node == 0:
            content['ok'] = u'主机名可以使用'
            return HttpResponse(json.dumps(content))
        else:
            content['error'] = u'主机名已存在'
            return HttpResponse(json.dumps(content))

@login_required
def node_filter(request):
    """
    分类检索
    """
    if request.method == 'GET':
        os = System_os
        number = room_hours
        idcs = IDC.objects.filter()
        get_data = request.GET.copy()

        vm = get_data.get('vm', None)
        idc = get_data.get('idc', '')
        os_param = get_data.get('os', '')
        Cabinets = get_data.get('Cabinets', '')
        room_param = get_data.get('room', '')
        #
        server_list = Host.objects.filter()
        centos_count = server_list.filter(system="CentOS")
        centos = 0
        debian = 0
        if vm:
            server_list = server_list.filter(vm=vm)
            centos = server_list.filter(vm=vm, system="CentOS")
        if idc:
            idc = int(idc)
            server_list = server_list.filter(idc__id=idc)
            centos += server_list.filter(idc__id=idc, system="CentOS").count()
        if os_param:
            if os_param == "Debian":
                server_list = server_list.filter(system=os_param)
                debian += server_list.count()
            else:
                server_list = server_list.filter(system=os_param)
                centos += server_list.count()
        if Cabinets:
            server_list = server_list.filter(Cabinets=Cabinets)
            centos += server_list.filter(Cabinets=Cabinets, system="CentOS").count()
        if room_param:
            server_list = server_list.filter(room_number=room_param)
            centos += server_list.filter(room_number=room_param, system="CentOS").count()


        server_list_count = server_list.count()
        debian = server_list_count - centos + debian
        return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))


@login_required
def server_delete(request):
    if request.method == 'POST':
        node_name = request.POST.get('node_name')
        node_name_list = node_name.split(',')
        node_list = []
        for name in node_name_list:
            try:
                node = Host.objects.get(node_name=name)
            except:
                msg = u"%s主机不存在" % name
                data = {'status': False, 'msg': msg}
                return HttpResponse(json.dumps(data))
            node_list.append(node)
        user = request.user
        for node in node_list:
            # 通知删除接口
            node.delete()
            token_api_id = token_id()
            list = salt_api_token({'client': 'wheel', 'fun': 'key.delete', 'match': node.node_name}, salt_api_url, {"X-Auth-Token": token_api_id})
            list.run()
            if node.edit_username:
                edit_username = node.edit_username
            else:
                edit_username = user.username
            idc_log(user.username, node.node_name, "删除", edit_username, node.edit_datetime, id, user.id)
        data = {'status': True, 'msg': '<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button><h4>已删除完毕,三秒后关闭</h4></div>'}
        return HttpResponse(json.dumps(data))

    else:
        node_name = request.GET.get('node_name', '')
        node_name_list = node_name.split(',')
        return render_to_response('assets/delete.html', locals(), context_instance=RequestContext(request))


@login_required
def server_id_delete(request,id):
    content = {}
    edit_id = Host.objects.get(id=id)
    # edit_username = ""
    if request.method == 'POST':    
        # 通知删除接口
        node = Host.objects.get(id=id)
        user = request.user
        node.delete()
        token_api_id = token_id()
        list = salt_api_token({'client': 'wheel', 'fun': 'key.delete', 'match': edit_id.node_name}, salt_api_url, {"X-Auth-Token": token_api_id})
        list.run()
        if node.edit_username:
            edit_username = node.edit_username
            idc_log(user.username, edit_id.node_name, "删除", edit_username, edit_id.edit_datetime, id, user.id)
        else:
            edit_username = user.username
            idc_log(user.username, edit_id.node_name, "删除", edit_username, edit_id.edit_datetime, id, user.id)
        data = {'status': True, 'msg': '<div class="alert alert-success alert-dismissable"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">×</button><h4>此主机已删除完毕,三秒后关闭</h4></div>'}
        return HttpResponse(json.dumps(data))
    else:
        return render_to_response('assets/delete.html', locals(), context_instance=RequestContext(request))

@login_required
def approve_list(request):
    if request.method == "POST":
        host_id_list = request.POST.getlist('approve_host')
        Host.objects.filter(id__in = host_id_list).update(vm=0)
    approve_list = Host.objects.filter(vm=-1)
    server_type = Project.objects.all()
    return render_to_response('assets/approve_vm.html', locals(), context_instance=RequestContext(request))


def batadd(request):
    """
    批量添加debian主机
    'idc', 'eth1', 'eth2', 'barnd', 'system', 'system_cpuarch', 'cabinet', 'editor', 'business', 'sort', 'use_for', 'service_line'
    """

    check_auth("bat_add_host")
    eth1 = request.GET['eth1']
    idc = 1
    brand = "Other"
    system = "Debian"
    system_cpuarch = "x86_64"
    editor = request.GET['editor']
    sort = "cloud"
    vm = 0
    host = Host(node_name=eth1, idc_id=idc, eth1=eth1, brand=brand, system=system,
                system_cpuarch=system_cpuarch,  editor=editor,
                sort=sort, vm=vm, status=1)
    test = host.save()
    if test:
        content = {"node_name": eth1, "idc": idc, "eth1": eth1, "brand": brand, "system": system,
                   "system_cpuarch": system_cpuarch, "editor": editor,
                   "sort": sort, "vm": vm}
    else:
        content = {"node_name": eth1}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4,))
# data = CustomUser(username=auth_username, is_staff=1, first_name=memberdata["fullname"], 
#             email=memberdata["mail"], department=auth_data["groups"], mobile=memberdata["mobile"], user_key=memberdata["key"])


def node_update(request):
    """
    添加资产方法
    """

    

        # uf = Host_from(request.POST)
    eth1 = request.GET['eth1']
    room_number = request.GET["room_number"]
    cabinet = request.GET["cabinet"]
    uses = request.GET["uses"]
    try:
        node = Host.objects.get(eth1=eth1)
        if node:
            node.eth1 = eth1
            node.room_number = room_number
            node.cabinet = cabinet
            node.uses = uses
            node.save()
            return HttpResponse(json.dumps({"status": "200", "result": "save is ok"}, ensure_ascii=False, indent=4,))
    except Host.DoesNotExist:
        return HttpResponse(json.dumps({"status": "404", "result": "over", "data": eth1}, ensure_ascii=False, indent=4,))
        
        # if uf.is_valid():
        #     # uf.save()
        #     #如果commit为False,则ManyToMany就需要使用以下方法
        #     zw = uf.save(commit=False)
        #     zw.edit_username = request.user.username
        #     zw.mac = str(request.POST.getlist("mac")[0]).replace(':', '-').strip(" ")
        #     zw.status = 0
        #     zw.vm = 0
        #     zw.save()
        #     return HttpResponseRedirect('/assets/server/')

@login_required
def server_order_by(request):
    if request.method == "POST":
        host_id_list = request.POST.get('list1SortOrder')
        for i in host_id_list:
            print i
    return HttpResponse(json.dumps({"status": "200", "result": "over",}, ensure_ascii=False, indent=4,))
    # return render_to_response('assets/approve_vm.html', locals(), context_instance=RequestContext(request))

@csrf_exempt
def install_ok(request):
    if request.method == "POST":
        sn = request.POST.get('sn')
        host = Host.objects.get(server_sn=sn)
        host.status = 1
        host.save()
    return HttpResponse(json.dumps({"status": "200", "result": "ok"}, ensure_ascii=False, indent=4,))

@login_required
def txt_update(request):
    cmdb_data = open("/home/www/cmdb/doc/cmdb.txt")

    for i in cmdb_data:
        i = i.split()
        ip = i[0]
        host = Host.objects.get(eth1=ip)
        host.eth1 = ip
        host.number = i[1]
        host.server_sn = i[2]
        host.Services_Code = i[3]
        host.save()

    cmdb_data.close()
    return HttpResponse(json.dumps({"status": "200", "result": "over"}, ensure_ascii=False, indent=4,))

