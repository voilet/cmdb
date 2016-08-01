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
from datetime import datetime

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404

from assets.models import  Project
from salt_ui.api.salt_token_id import *
from mysite.settings import salt_api_url, pxe_url_api
from assets.models import Host

#日志记录
#登录
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from salt_ui.api.salt_https_api import pxe_api
import requests, json
from config.models import Salt_mode_name
from salt_ui.models import SetupLog
from assets.models import Line
from django import forms
from django.http import HttpResponse
from cmdb_auth.no_auth import check_auth
from assets.value_class.idc_api import host_all


@login_required
def auto_index(request):
    status = check_auth(request, "auth_highstate")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    content = {}
    line_list = Line.objects.filter()
    content["line_list"] = line_list
    content["business_noline"] = Project.objects.filter(line__isnull=True)
    content.update(csrf(request))
    data = host_all()

    return render_to_response('autoinstall/install_list.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def services_install_init(request):
    content = {}
    server_list = Host.objects.filter(status=1).order_by("-id")
    server_type = Project.objects.all()
    content["server_type"] = server_type
    content["list"] = server_list
    try:
        if "token_id" in request.COOKIES["token_id"]:
            token_api_id = request.COOKIES["token_id"]
        else:
            token_api_id = token_id()
    except KeyError:
        token_api_id = token_id()

    if request.method == 'POST':
        node_hostname = request.POST
        node_name = node_hostname.getlist("hostname_id")
        # for i in node_name:
        list_all = salt_api_token({'fun': 'state.highstate', 'tgt': node_name, 'expr_form':'list'}, salt_api_url, { 'X-Auth-Token' : request.COOKIES["token_id"]})
        list_all = list_all.run()
        for i in list_all["return"]:
            content["jid"] =  i["jid"]
            content["minions"] = i["minions"]
        jobs_id = content["jid"]
        jobs_url = salt_api_url + "jobs/" + jobs_id
        print type(jobs_url)
        headers = {'content-type': 'application/json', 'X-Auth-Token': '4f70afcded3e4c44c2303e75b02e5846e24cb029'}
        r = requests.get(jobs_url, headers=headers,)
        print type(r.url)
        print r.text
        print json.loads(r.text)
        # minions_list_all = salt_api_jobs(
        # jobs_url,
        # {"X-Auth-Token": token_api_id}
        # )
        # voilet_test = minions_list_all.run()
        # print yaml.dump(voilet_test)
        content.update(csrf(request))
        return render_to_response('autoinstall/install_init.html', content, context_instance=RequestContext(request))

    content.update(csrf(request))
    response= render_to_response('autoinstall/install_init.html', content, context_instance=RequestContext(request))
    try:
        if "token_id" not in request.COOKIES["token_id"]:
            response.set_cookie('token_id', token_api_id, expires=4*60*60)
    except KeyError:
        response.set_cookie('token_id', token_api_id, expires=4*60*60)
    return response

class Sls_from(forms.ModelForm):
    class Meta:
        model = Salt_mode_name
        fields = "__all__"

@login_required
@csrf_protect
def sls_install_init(request):
    content = {}
    server_list = Host.objects.filter(status=1).order_by("-id")
    sls_name = Salt_mode_name.objects.all()
    if request.method == 'POST':
        node_hostname = request.POST
        node_name = node_hostname.getlist("hostname_id")
        sls = node_hostname.getlist("sls")
    content['sls'] = sls_name
    content['node'] = server_list
    content.update(csrf(request))
    return render_to_response('autoinstall/install_sls.html', content, context_instance=RequestContext(request))



@login_required
@csrf_protect
def services_install_all(request):
    content = {}
    server_list = Host.objects.filter(status=0).order_by("-create_time")
    server_type = Project.objects.all()
    content["server_type"] = server_type
    content["list"] = server_list
    if request.method == 'POST':
        node_hostname = request.POST
        hostname_id = node_hostname.getlist("hostname_id")
        setup_error = []
        for i in hostname_id:
            host_list = Host.objects.get(id=i)
            '''向pxe提交数据'''
            pxe_url = pxe_url_api + "create-physical-instances"
            pxe_data = pxe_api({
                "hostname": host_list.node_name.strip(),
                "operating": host_list.system.lower() + "_6u4_64".strip(),
                "mac": host_list.mac.strip(),
                "usage": host_list.usage,
                "model": host_list.brand.lower().strip(),
            }, pxe_url)
            pxe_post_data = json.loads(pxe_data.run())
            if pxe_post_data["status"] == 200:
                host_list.status = 1
                host_list.save()
            else:
                setup_error.append(pxe_post_data)
                host_list.status = 0
                host_list.save()
        content["error"] = True
        content["data"]=setup_error
        content.update(csrf(request))
        if "jumeiops" in request.request.user.department or "admin" in request.user.department:
            return render_to_response('autoinstall/install_system.html', content, context_instance=RequestContext(request))
        else:
            return render_to_response('user/auth_error_index.html', content, context_instance=RequestContext(request))
    return render_to_response('autoinstall/install_system.html', content, context_instance=RequestContext(request))


@login_required
@csrf_protect
def services_install_setup_node(request):
    """安装系统"""
    content = {}
    if request.method == 'POST':
        node_hostname = request.POST
        hostname_id = node_hostname.getlist("hostname_id")
        for i in hostname_id:
            host_list = Host.objects.get(uuid=str(i))
            # 向pxe提交数据
            pxe_url = pxe_url_api + "create-physical-instances"
            pxe_data = pxe_api({
                "ip": host_list.eth1,
                "mac": host_list.mac,
                "brand": host_list.brand,
            }, pxe_url)

            test = pxe_data.run()
            pxe_post_data = json.loads(test)
            print pxe_post_data
            if pxe_post_data["status"] == 200:
                host_list.status = 2
                # host_list.save()
                content["return"] = True
                content["result"] = pxe_post_data["result"]
                content.update(csrf(request))
                return render_to_response('autoinstall/auto_setup_system_error.html', locals(), context_instance=RequestContext(request))
            else:
                content["return"] = False
                content["result"] = pxe_post_data["result"]
                host_list.status = 0
                host_list.save()
                content.update(csrf(request))
                return render_to_response('autoinstall/auto_setup_system_error.html', locals(), context_instance=RequestContext(request))
    return render_to_response('autoinstall/install_list.html', content, context_instance=RequestContext(request))

@login_required
def sls_install_id(request, id):
    """
    salt自动推送业务，使用expr_form有弊端，需要读取jobsid才可看到返回内容，此方法可能需要重构
    """
    content = {}
    node_name = []
    business_list = []
    business = Project.objects.get(id=id)
    user_list = request.user
    user_business = user_list.all_business.values("service_name")
    for i in user_business:
        i = u"%s" % (i["service_name"])
        business_list.append(i)
    # 判断用户是否有当前业务权限
    if business.service_name in business_list:
        node = business.host_set.all()
        for node_key in node:
            if node_key.status == 1:
                node_name.append(node_key.node_name)
        node_name = ",".join(node_name)

        token_api_id = token_id()
        list_all = salt_api_token({'client': 'local', 'fun': 'state.highstate', 'mode':"async", 'tgt': node_name, 'expr_form': 'list'}, salt_api_url, {'X-Auth-Token': token_api_id})
        list_all = list_all.run()
        setup_all = {}
        setup_return = {}
        setup_status = {}
        list_all["return"]
        #return jid
        content["setup_node"] = len(node_name)
        content["setup_down"] = [node_true for node_true in node_name if node_true not in setup_return.keys()]
        content["setup_error"] = len(content["setup_down"])
        content["setup_status"] = setup_status
        content["setup_return"] = setup_return
        #content["connect"] = data
        content.update(csrf(request))
        return render_to_response('autoinstall/install_setup_list.html', content, context_instance=RequestContext(request))
    else:
        return render_to_response('autoinstall/install_setup.html', content, context_instance=RequestContext(request))




class SetupLogForm(forms.ModelForm):
    class Meta:
        model = SetupLog
        fields = ['business', 'content']


@login_required
@csrf_protect
def apply_install(request):
    """申请自动推送配置文件"""
    if request.method == "POST":#提交申请
        log_form = SetupLogForm(request.POST)
        if log_form.is_valid():
            log = log_form.save(commit=False)
            user_list = request.user
            log.user = user_list
            log.status = 1
            log.save()
            log.business.status=1
            log.business.save()
            return HttpResponseRedirect('/auto/setup/')
        return HttpResponseRedirect('/auto/apply/')
    else:#显示可以推送的项目
        form = SetupLogForm()
        content = {'form':form}
        if "jumeiops" in request.user.department:
            user_list = request.user
            temp_list = ProjectUser.objects.filter(user = request.user)
            user_business = [one.myform for one in temp_list]
            content['user_business'] = user_business
            content.update(csrf(request))
            return render_to_response('autoinstall/apply_install.html', content, context_instance=RequestContext(request))
        elif "admin" in request.user.department:
            content['user_business'] = Project.objects.all()
            content.update(csrf(request))
            return render_to_response('autoinstall/apply_install.html', content, context_instance=RequestContext(request))
    return render_to_response('autoinstall/apply_install.html', locals(), context_instance=RequestContext(request))

@login_required()
def approve_install(request):
    #审批配置发送请求
    if "admin" not in request.user.department:
        return HttpResponse(u"没有权限")
    apply_id = request.GET.get('apply_id',0)
    if apply_id:
        apply_item = get_object_or_404(SetupLog,pk=apply_id)
        apply_item.status=2
        apply_item.approve_user =request.user
        apply_item.approve_time = datetime.now()
        apply_item.save()

        return HttpResponse('ok')
    apply_list = SetupLog.objects.filter(status=1)
    content={}
    content['apply_list'] = apply_list
    return render_to_response('autoinstall/approve_install.html', content, context_instance=RequestContext(request))


@login_required()
@csrf_protect
def reject_apply(request):
    #拒绝推送，写原因
    if request.method == "POST":
        print 'ddd'
        apply_id = request.POST.get('apply_id',0)
        reason = request.POST.get('reject_reason','')
        apply_item = get_object_or_404(SetupLog,pk=apply_id)
        apply_item.status=0
        apply_item.approve_user =request.user
        apply_item.approve_time = datetime.now()
        apply_item.reject_reason = reason
        apply_item.save()

        return HttpResponseRedirect('/auto/approve/')


@login_required
def sls_install_setup(request):
    """
    显示可自动推送所有配置文件的项目
    该操作设定只有jumeiops和admin两个组可以操作
    """
    content = {}
    if "jumeiops" in request.user.department:
        user_business = SetupLog.objects.filter(user=request.user,status=0)
        content['user_business'] = user_business
        content.update(csrf(request))
        return render_to_response('autoinstall/install_setup.html', content, context_instance=RequestContext(request))
    elif "admin" in request.request.user.department:
        user_business = SetupLog.objects.filter(status=0)
        content['user_business'] = user_business
        content['business'] = Project.objects.all()
        content.update(csrf(request))
        return render_to_response('autoinstall/install_setup.html', content, context_instance=RequestContext(request))
    else:
        return render_to_response('user/auth_error_index.html', content, context_instance=RequestContext(request))

@login_required
def install_id_setup(request, id):
    """
    根据业务来进行推送安装
    真正的推送在sls_install_id这个函数中。。。这个混乱的逻辑，无数次的权限检查啊
    """
    content = {}
    node_name = []
    business_list = []
    business = Project.objects.get(id=id)
    if "jumeiops" in request.user.department:
        user_list = request.user
        user_business = user_list.all_business.values("service_name")
        for i in user_business:
            i = u"%s" % (i["service_name"])
            business_list.append(i)
        # 判断用户是否有当前业务权限
        if business.service_name in business_list:
            node = business.host_set.all()
            for node_key in node:
                if node_key.status == 1:
                    node_name.append(node_key.node_name)
            content["business"] = business.service_name
            content["node"] = node_name
            content["node_count"] = len(node_name)
            content["setup_id"] = id
            content.update(csrf(request))
            return render_to_response('autoinstall/install_setup_list_count.html', content, context_instance=RequestContext(request))
    elif "admin" in request.user.department:
        admin_node = Host.objects.filter(business=business)
        for i in admin_node:
            if i.status == 1:
                node_name.append(i.node_name)
        content["business"] = business.service_name
        content["node"] = node_name
        content["node_count"] = len(node_name)
        content["setup_id"] = id
        content.update(csrf(request))
        return render_to_response('autoinstall/install_setup_list_count.html', content, context_instance=RequestContext(request))
    else:
        return HttpResponse("无权限使用")


def log_list(request,pk):
    """
    用于ajax请求，返回历史推送记录和提交form
    """
    business = get_object_or_404(Project,pk=pk)
    log_list = SetupLog.objects.filter(business=business).order_by('-id')
    business_status = True
    if log_list:
        business_status = log_list[0].status==0
    return render_to_response('autoinstall/../../templates/config/log_list.html', locals(), context_instance=RequestContext(request))


@login_required
def install_by_name_list(request):
    """
        located in aoto_index page with parameter ,which is a list of host name selected
    """
    name_list = request.POST.get('name_list')
    node_name = ",".join(name_list)
    token_api_id = token_id()
    list_all = salt_api_token({'client': 'local', 'fun': 'state.highstate', 'mode':"async", 'tgt': node_name, 'expr_form': 'list'}, salt_api_url, {'X-Auth-Token': token_api_id})
    list_all = list_all.run()
    return render_to_response('autoinstall/install_setup_list.html', locals(), context_instance=RequestContext(request))

