# coding=UTF-8
import datetime
import os
import re
# import md5
import json

from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
import commands, json, yaml
from assets.models import Project
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import salt_api_pass, salt_api_user, salt_api_url, pxe_url_api, auth_content, app_key, app_name, \
    auth_url, auth_key
from assets.models import Host
import hashlib, time
# 日志记录
from salt_ui.views.api_log_class import salt_log
from swan.models import SwanLog
# 登录
from users.models import CustomUser
import requests
from django.contrib.auth import authenticate, login
from accounts.models import UserCreateForm
from utils.user_help import *
from assets.models import Line, IDC, Host, project_swan
from assets.value_class.idc_api import host_all
from users.models import department_Mode
from malfunction.models import Incident
from assets.ztree.service import ztree_tag
from api.api import Date_time


# songxs add
@login_required
def salt_index(request):
    line_list = Line.objects.filter()
    business = Project.objects.filter(line__isnull=False)
    no_business = Project.objects.filter(line__isnull=True)
    # business = Project.objects.all()

    data = host_all()
    ztree_data = ztree_tag(request.user.username)

    idc_count = IDC.objects.all()

    idc_data = {}
    for idc in idc_count:
        idc_data[idc.name] = Host.objects.filter(idc=idc).count()
    user_count = CustomUser.objects.filter().count()

    department_count = department_Mode.objects.filter().count()
    # idc = IDC.objects.get(uuid='9cd9516af1454c619af617d92050fc99')
    # f = open("/Users/voilet/python_code/cmdb/doc/cmdb.txt", "r")
    # s = f.readlines()
    # for i in s:
    #     i = i.split()
    #     t = Host(eth1=i[0], number=i[1], Services_Code=i[3], server_sn=i[2], status=1, brand=u'Dell R420',
    #              idc=idc, system=u"CentOS")
    #     t.save()
    # f.close()

    return render_to_response('default/default.html', locals(), context_instance=RequestContext(request))


@login_required
def salt_index_new(request):
    line_list = Line.objects.all()
    if line_list.count() == 0:
        return HttpResponseRedirect('/assets/product/add/?init=true')

    ztree_data = ztree_tag(request.user.username)
    users = CustomUser.objects.count()
    hosts = Host.objects.count()
    problems = Incident.objects.count()
    project = Project.objects.count()
    idc_count = IDC.objects.all().count()
    if idc_count == 0:
        return HttpResponseRedirect('/assets/idc_add/?init=true')
    if project == 0:
        return HttpResponseRedirect('/assets/server/type/add/?init=true')
    if hosts == 0:
        return HttpResponseRedirect('/assets/host_add/?init=true')
    swan_count = project_swan.objects.count()
    swan_log_data = SwanLog.objects.all().order_by("-swan_datetime")
    swan_log = swan_log_data[:10]
    start_time, stop_time = Date_time()
    swan_push_data = SwanLog.objects.filter(swan_datetime__gte=stop_time)
    swan_data = {}
    for i in swan_push_data:
        project_name = i.project_name
        if swan_data.get(project_name, False):
            swan_data[i.project_name]["count"] += 1
        else:
            swan_data[i.project_name] = {"count": 1, "uuid": i.project_uuid}
    # for k, v in swan_data.items():
    #     print k, v
    return render_to_response('default/default_new.html', locals(), context_instance=RequestContext(request))


def OpsDoc(request):
    line_list = Line.objects.filter()
    business = Project.objects.filter(line__isnull=False)
    no_business = Project.objects.filter(line__isnull=True)
    ztree_data = ztree_tag(request.user.username)
    users = CustomUser.objects.all().count()
    hosts = Host.objects.all()
    problems = Incident.objects.all().count()
    project = Project.objects.all().count()
    swan_count = project_swan.objects.all().count()
    swan_log = SwanLog.objects.all().order_by("-swan_datetime")[:10]
    return render_to_response('default/markdown.html', locals(), context_instance=RequestContext(request))


def salt_help(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('saltstack/salt_help.html', context_instance=RequestContext(request))


def test(request):
    context = {}
    context.update(csrf(request))
    return render_to_response('saltstack/editor.html', context_instance=RequestContext(request))


def auth_login(request):
    content = {}
    auth_token_id = request.GET['token']
    auth_username = request.GET['username']
    auth_login_url = "%s%s%s%s%s" % (auth_url, "/api/grouprole/?uid=", auth_username, app_key, app_name)
    headers = {'content-type': 'application/json'}
    auth_result = requests.get(auth_login_url, headers=headers)
    auth_data = auth_result.json()
    if len(auth_data["groups"]) > 0:
        content["Role"] = auth_data["groups"]
        memberurl = "%s%s%s%s%s" % (auth_url, "api/member/?uid=", auth_username, app_key, app_name)
        headers = {'content-type': 'application/json'}
        member_result = requests.get(memberurl, headers=headers, )
        memberdata = member_result.json()
        if CustomUser.objects.filter(username=auth_username).count() == 0:
            try:
                data = CustomUser(username=auth_username, is_staff=1, first_name=memberdata["fullname"],
                                  email=memberdata["mail"], department=auth_data["groups"], mobile=memberdata["mobile"],
                                  user_key=memberdata["key"])
            except KeyError:
                data = CustomUser(username=auth_username, is_staff=1, first_name=memberdata["fullname"],
                                  email=memberdata["mail"], department=auth_data["groups"], mobile=memberdata["mobile"],
                                  user_key="")
            data.save()
            user_list = CustomUser.objects.get(username=auth_username)
            user_list.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user_list)
            request.session.set_expiry(60 * 60 * 3)
            content.update(csrf(request))
            return HttpResponseRedirect('/')
        else:
            salt_data = CustomUser.objects.get(username=auth_username)
            salt_data.first_name = memberdata["fullname"]
            salt_data.email = memberdata["mail"]
            salt_data.department = auth_data["groups"]
            salt_data.mobile = memberdata["mobile"]
            try:
                salt_data.user_key = memberdata["key"]
            except KeyError:
                salt_data.user_key = ""
            salt_data.save()
            salt_data.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, salt_data)
            session_id = hashlib.sha1(auth_token_id + auth_key + auth_username).hexdigest()
            user_list = CustomUser.objects.get(username=auth_username)
            request.session.set_expiry(60 * 60 * 3)
            content.update(csrf(request))
            return HttpResponseRedirect('/')
    else:
        return render_to_response('default/error.html')


@login_required
def salt_cmd_commands(request):
    """
    执行cmd命令
    """
    context = {}
    user_node_list = []
    user_id = request.user

    myform_list = get_business_by_user(request.user)
    for server_type_node in myform_list:
        user_node = server_type_node.host_set.all()
        user_node_list.append({server_type_node: user_node})
    context["node_list"] = user_node_list
    context['service_name'] = myform_list
    context["user"] = user_id
    context.update(csrf(request))
    return render_to_response('saltstack/salt_cmd.html', context, context_instance=RequestContext(request))


@login_required
def status(request):
    """
    列出所有认证过的主机，将主机和当前资产库做对比，不在资产库里的主机提示需上报资产
    """
    context = {}
    node_name_update = []
    node_name_all = [one.node_name for one in Host.objects.only("node_name")]
    token_api_id = token_id()
    list_all = salt_api_token(
        {
            'client': 'wheel',
            'fun': 'key.list_all',
        },
        salt_api_url,
        {"X-Auth-Token": token_api_id}
    )
    list_all = list_all.run()
    print list_all
    data = list_all['return'][0]
    print data
    if data['data']['success']:
        return_data = data['data']['return']
        minions = return_data['minions']

    for node in minions:
        if node not in node_name_all:
            node_name_update.append(node)
    context["node_name_update"] = node_name_update
    context.update(csrf(request))
    return render_to_response('saltstack/node_status.html', locals(), context_instance=RequestContext(request))


@login_required
def salt_node_list(request):
    """
    列出所有已经过认证的主机列表
    """
    context = {}
    token_api_id = token_id()
    list = salt_api_token({"client": 'wheel', "fun": "key.list_all",}, salt_api_url, {"X-Auth-Token": token_api_id})
    list = list.run()
    for i in list["return"]:
        minions = i["data"]["return"]["minions"]
    context["salt_key"] = minions
    context.update(csrf(request))
    return render_to_response('saltstack/node_list.html', context, context_instance=RequestContext(request))


@login_required
@csrf_protect
def salt_cmd(request):
    """CMD选项功能"""
    context = {}
    salt_node_name = ""
    salt_node_name_null = ""
    node_list = []
    if request.method == 'POST':
        salt_text = request.POST
        business_node = salt_text.getlist("business_node")
        for i in business_node:
            i = '%s' % (i)
            node_list.append(i.encode("utf-8"))
        salt_api_type = salt_text['comm_shell']
        # 选择cmd类型执行方法
        if salt_api_type == "cmd":
            salt_cmd_lr = salt_text['salt_cmd']
            # 如果使用危险命令则返回无权限
            if str(salt_cmd_lr).split()[0] in auth_content:
                context["auth_content"] = True
                context.update(csrf(request))
                return render_to_response('saltstack/salt_cmd_run.html', context,
                                          context_instance=RequestContext(request))
            # 是可指定主机，注意，此权限较高
            if "salt_node_name" in salt_text:
                if len(business_node) > 0 and len(salt_text["salt_node_name"]) > 0:
                    node_list.append(salt_text["salt_node_name"])
                elif len(business_node) > 0 and len(salt_text["salt_node_name"]) == 0:
                    node_list = business_node
                elif len(business_node) == 0 and len(salt_text["salt_node_name"]) > 0:
                    salt_node_name_null += salt_text["salt_node_name"]
                elif len(salt_text["salt_node_name"]) > 0:
                    node_list = salt_text["salt_node_name"]
                else:
                    salt_node_name_null += "*"
            else:
                node_list = business_node
            token_api_id = token_id()
            if len(node_list) >= 2:
                list_all = salt_api_token({'fun': 'cmd.run', 'tgt': node_list,
                                           'arg': salt_cmd_lr, 'expr_form': 'list'},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                list_all = list_all.run()
                # time.sleep(5)
                for i in list_all["return"]:
                    context["jid"] = i["jid"]
                    context["minions"] = i["minions"]
                    jobs_id = context["jid"]
                    jobs_url = salt_api_url + "/jobs/" + jobs_id
                    minions_list_all = salt_api_jobs(
                        jobs_url,
                        {"X-Auth-Token": token_api_id}
                    )
                    voilet_test = minions_list_all.run()
                    for i in voilet_test["return"]:
                        context["cmd_run"] = i
                        context["cmd_Advanced"] = False
                        context["salt_cmd"] = salt_text['salt_cmd']
                        context["len_node"] = len(i.keys())
                    context.update(csrf(request))
                    # 日志入库
                    salt_log(request.user.username, context["minions"], int(jobs_id),
                             salt_api_type, context["len_node"], salt_cmd_lr, context["cmd_run"])
                    return render_to_response('saltstack/salt_cmd_run.html', context,
                                              context_instance=RequestContext(request))
            elif len(node_list) == 1:
                list_all = salt_api_token({'client': 'local', 'fun': 'cmd.run',
                                           'tgt': node_list, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                voilet_test = list_all.run()
                for i in voilet_test["return"]:
                    # print i.keys()
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # 日志入库
                salt_log(request.user.username, context["minions"], '', salt_api_type,
                         context["len_node"], salt_cmd_lr, context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_run.html', context,
                                          context_instance=RequestContext(request))
            elif salt_node_name:
                list_all = salt_api_token({'client': 'local', 'fun': 'cmd.run',
                                           'tgt': salt_node_name, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                voilet_test = list_all.run()
                for i in voilet_test["return"]:
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # 日志入库
                salt_log(request.user.username, context["minions"], '',
                         salt_api_type, context["len_node"], salt_cmd_lr, context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_run.html', context,
                                          context_instance=RequestContext(request))
            elif salt_node_name_null:
                list_all = salt_api_token({'client': 'local', 'fun': 'cmd.run',
                                           'tgt': salt_node_name_null, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                list_all = list_all.run()
                for i in list_all["return"]:
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # print yaml.dump(context["cmd_run"])
                # 日志入库
                salt_log(request.user.username, context["minions"], '', salt_api_type, context["len_node"], salt_cmd_lr,
                         context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_run.html', context,
                                          context_instance=RequestContext(request))
            elif len(node_list) == 0:
                context["cmd_Advanced"] = False
                context.update(csrf(request))
                return render_to_response('saltstack/salt_cmd_run.html', context,
                                          context_instance=RequestContext(request))
        # 如果选择类型是grains
        elif salt_api_type == "grains":
            salt_cmd_lr = salt_text['salt_cmd']
            if "salt_node_name" in salt_text:
                if len(business_node) > 0 and len(salt_text["salt_node_name"]) > 0:
                    node_list.append(salt_text["salt_node_name"])
                elif len(business_node) > 0 and len(salt_text["salt_node_name"]) == 0:
                    node_list = business_node
                elif len(business_node) == 0 and len(salt_text["salt_node_name"]) > 0:
                    salt_node_name += salt_text["salt_node_name"]
                elif len(salt_text["salt_node_name"]) > 0:
                    node_list = salt_text["salt_node_name"]
                else:
                    salt_node_name_null += "*"
            else:
                node_list = business_node
            token_api_id = token_id()
            if len(node_list) >= 2:
                list_all = salt_api_token({'fun': 'grains.item', 'tgt': node_list,
                                           'arg': salt_cmd_lr, 'expr_form': 'list'},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                list_all = list_all.run()
                for i in list_all["return"]:
                    context["jid"] = i["jid"]
                    context["minions"] = i["minions"]
                    jobs_id = context["jid"]
                    jobs_url = salt_api_url + "/jobs/" + jobs_id
                    minions_list_all = salt_api_jobs(
                        jobs_url,
                        {"X-Auth-Token": token_api_id}
                    )
                    voilet_test = minions_list_all.run()
                    for i in voilet_test["return"]:
                        context["cmd_run"] = i
                        context["cmd_Advanced"] = False
                        context["salt_cmd"] = salt_text['salt_cmd']
                        context["len_node"] = len(i.keys())
                    context.update(csrf(request))
                    # 日志入库
                    salt_log(request.user.username, context["minions"], int(jobs_id),
                             salt_api_type, context["len_node"], salt_cmd_lr, context["cmd_run"])
                    return render_to_response('saltstack/salt_cmd_grains_run.html',
                                              context, context_instance=RequestContext(request))
            elif len(node_list) == 1:
                list_all = salt_api_token({'client': 'local', 'fun': 'grains.item',
                                           'tgt': node_list, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                voilet_test = list_all.run()
                for i in voilet_test["return"]:
                    # print i.keys()
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # 日志入库
                salt_log(request.user.username, context["minions"], '', salt_api_type,
                         context["len_node"], salt_cmd_lr, context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_grains_run.html', context,
                                          context_instance=RequestContext(request))
            elif salt_node_name:
                list_all = salt_api_token({'client': 'local', 'fun': 'grains.item',
                                           'tgt': salt_node_name, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                voilet_test = list_all.run()
                for i in voilet_test["return"]:
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # 日志入库
                salt_log(request.user.username, context["minions"], '',
                         salt_api_type, context["len_node"], salt_cmd_lr, context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_grains_run.html', context,
                                          context_instance=RequestContext(request))
            elif salt_node_name_null:
                list_all = salt_api_token({'client': 'local', 'fun': 'grains.item',
                                           'tgt': salt_node_name_null, 'arg': salt_cmd_lr},
                                          salt_api_url, {'X-Auth-Token': token_api_id})
                list_all = list_all.run()
                for i in list_all["return"]:
                    context["cmd_run"] = i
                    context["cmd_Advanced"] = False
                    context["salt_cmd"] = salt_text['salt_cmd']
                    context["len_node"] = len(i.keys())
                    context["minions"] = i.keys()
                context.update(csrf(request))
                # 日志入库
                salt_log(request.user.username, context["minions"], '',
                         salt_api_type, context["len_node"], salt_cmd_lr, context["cmd_run"])
                return render_to_response('saltstack/salt_cmd_grains_run.html', context,
                                          context_instance=RequestContext(request))
            elif len(node_list) == 0:
                context["cmd_Advanced"] = False
                context.update(csrf(request))
                return render_to_response('saltstack/salt_cmd_grains_run.html',
                                          context, context_instance=RequestContext(request))
        else:
            return render_to_response('saltstack/salt_cmd_run.html', context, context_instance=RequestContext(request))


@login_required
@csrf_protect
def salt_garins(request):
    context = {}
    if request.method == 'POST':
        salt_text = request.POST
        if salt_text['salt_cmd']:
            salt_cmd_lr = salt_text['salt_cmd']
            salt_node_name = salt_text["salt_node_name"]
            token_api_id = token_id()
            list_all = salt_api_token(
                {
                    'client': 'local',
                    'fun': 'grains.item',
                    'tgt': salt_node_name,
                    'arg': salt_cmd_lr,
                },
                salt_api_url,
                {"X-Auth-Token": token_api_id}
            )
            list_all = list_all.run()
            for i in list_all["return"]:
                context["cmd_run"] = i
            context["cmd_Advanced"] = False
            context["salt_cmd"] = salt_text['salt_cmd']
            context.update(csrf(request))
            return render_to_response('saltstack/salt_cmd_grains_run.html', context,
                                      context_instance=RequestContext(request))
            #     #return HttpResponse(json.dumps(cmd))

    else:
        context.update(csrf(request))
        return render_to_response('saltstack/salt_garins.html', context, context_instance=RequestContext(request))


# salt_node_shell
@login_required
@csrf_protect
def salt_check_setup(request):
    context = {}
    if request.method == 'POST':
        salt_text = request.POST
        salt_cmd_lr = salt_text['salt_shell_node']
        cmd = commands.getoutput("salt-ssh " + salt_cmd_lr + " state.sls check_install")
        context['salt_cmd'] = cmd
        context["cmd_Advanced"] = True
        context.update(csrf(request))
        return render_to_response('saltstack/salt_check_setup.html', context, context_instance=RequestContext(request))


# salt_node_shell
@login_required
@csrf_protect
def salt_state_sls(request):
    context = {}
    if request.method == 'POST':
        salt_text = request.POST
        salt_cmd_lr = salt_text['salt_sls']
        node = salt_text["salt_node"]
        token_api_id = token_id()
        list_all = salt_api_token(
            {
                'client': 'local',
                'fun': 'state.sls',
                'tgt': node,
                'arg': salt_cmd_lr,
            },
            salt_api_url,
            {"X-Auth-Token": token_api_id}
        )
        list_all = list_all.run()
        test = yaml.dump(list_all["return"])
        context["salt_cmd"] = test
        context["cmd_Advanced"] = True
        context.update(csrf(request))
        # return HttpResponse(json.dumps(context["salt_cmd"]),context_instance=RequestContext(request))
        return render_to_response('saltstack/salt_check_setup.html', context, context_instance=RequestContext(request))
    else:
        context["cmd_Advanced"] = False
        context.update(csrf(request))
        return render_to_response('saltstack/salt_state_sls.html', context, context_instance=RequestContext(request))
