#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
============================================================================
FileName: views.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 2014-03-05
     History:
=============================================================================
"""


# 日志记录
# 登录
from django.contrib.auth.decorators import login_required
import time
import json
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from users.models import CustomUser
from django.core.mail import send_mail
from mysite.settings import websocket_url
from swan.swan_api import swan_push_api
from users.models import department_Mode
from assets.models import Project
from swan.models import Apply, SwanLog
from assets.models import project_swan
from assets.models import Host
from mysite.settings import auth_key
from cmdb_auth.no_auth import check_auth
import ast
import hashlib
import datetime
import uuid
from users.models import CustomUser


def token(auth_key, id, username, project, module):
    token = hashlib.sha1(auth_key + str(id) + username + project + module).hexdigest()
    return token


def swan_push(request):
    """

    :param requests:
    :return:
    """
    sls = request.GET.get("sls")
    if request.method == 'POST':
        test = request.POST
        t = test.getlist("node_name")
        pull_list = []
        for i in t:
            t_data = Host.objects.get(node_name=i)
            pull_list.append({"ip": t_data.eth1, "fqdn": t_data.node_name})
        s = swan_push_api(sls)
        if s["status"] == 200:
            return render_to_response('swan/push.html', locals(), context_instance=RequestContext(request))

    return HttpResponse(json.dumps({"status": "403", "message": "Authentication failed"}, ensure_ascii=False, indent=4))
    # return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_index(request):
    status = check_auth(request, "auth_project")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    swan_data = Project.objects.all()

    return render_to_response('swan/index.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_release(request):
    if request.method == 'POST':
        uid = str(uuid.uuid4())
        rst = request.POST
        # print rst
        project_name = rst.get("project_name", False)
        project_all_tag = rst.get("project_all_tag", False)
        tgt = rst.get("tgt", False)
        arg = rst.get("arg", False)
        log = rst.get("update_log", None)
        # print update_log
        business_id = Project.objects.get(uuid=project_name)
        server_list = {}
        ip_list = []
        node_list = business_id.host_set.all()
        # 根据项目名反查主机
        if len(rst.getlist("node_name")) == 0:
            return render_to_response('swan/swan_error.html', locals(), context_instance=RequestContext(request))
        else:
            for i in rst.getlist("node_name"):
                s = node_list.get(eth1=i)
                server_list[s.eth1] = s.node_name
                ip_list.append(s.eth1)
        # if arg:
        #     return render_to_response('swan/swan_error.html', locals(), context_instance=RequestContext(request))
        # 将所查数据post tornado接口进行异步操作
        swan_data = project_swan.objects.get(uuid=project_all_tag)
        choose = int(swan_data.choose)
        if choose == 2 or choose == 3:
            try:
                git_minion = swan_data.git_code.codeFqdn
            except:
                git_minion = False
            try:
                git_code_user = swan_data.git_code_user
            except:
                git_code_user = "root"
            try:
                git_minion_path = swan_data.git_code.codePath
            except:
                git_minion_path = ""
            try:
                tomcat_init = swan_data.tomcat_init
            except:
                tomcat_init = ""
            try:
                cache = swan_data.cache
            except:
                cache = ""

            data = {
                "choose": choose,
                "code_name": swan_data.code_name,
                "arg": arg,
                "host": server_list,
                "ip_data": ip_list,
                "uid": uid,
                "git_minion": git_minion,
                "git_minion_path": git_minion_path,
                "git_version": tgt,
                "code_path": swan_data.code_path,
                "reset_code": rst.get("reset_code"),
                "git_code_user": git_code_user,
                "tomcat_init": tomcat_init,
                "cache": cache,
                "CheckUrl": swan_data.CheckUrl,
                "tgt": tgt,
                "shell_status": swan_data.shell_status,
                "shell": swan_data.shell,
            }
        elif choose == 4:
            try:
                git_minion = swan_data.git_code.codeFqdn
            except:
                git_minion = False
            try:
                git_code_user = swan_data.git_code_user
            except:
                git_code_user = "root"
            try:
                git_minion_path = swan_data.git_code.codePath
            except:
                git_minion_path = ""
            data = {
                "choose": swan_data.choose,
                "code_name": swan_data.code_name,
                "arg": arg,
                "host": server_list,
                "ip_data": ip_list,
                "uid": uid,
                "git_minion": git_minion,
                "git_minion_path": git_minion_path,
                "git_version": tgt,
                "code_path": swan_data.code_path,
                "reset_code": rst.get("reset_code"),
                "git_code_user": git_code_user,
                "shell": swan_data.shell,
                "CheckUrl": swan_data.CheckUrl,
                "tgt": tgt,
                "shell_status": swan_data.shell_status,
            }

        else:
            data = {
                "choose": choose,
                "sls": swan_data.salt_sls,
                "check_port_status": swan_data.check_port_status,
                "check_port": swan_data.check_port,
                "bat_push": swan_data.bat_push,
                "script": swan_data.script,
                "tgt": tgt,
                "argall_str": swan_data.argall_str,
                "code_name": swan_data.code_name,
                "arg": arg,
                "host": server_list,
                "ip_data": ip_list,
                "CheckUrl": swan_data.CheckUrl,
                "uid": uid,
                "shell_status": swan_data.shell_status,
                "shell": swan_data.shell,
            }
        s = swan_push_api(data)
        if s["status"] == 200:
            try:
                log_data = SwanLog(username=request.user.first_name,
                              userID=request.user.uuid,
                              project_name=business_id.service_name,
                              project_uuid=str(business_id.uuid),
                              module_name=tgt,
                              module_args=arg,
                              swan_name=swan_data.swan_name,
                              status=True,
                              message=u'发布成功',
                              update_log=log

                              )
                log_data.save()
            except:
                pass
            return HttpResponse(
                json.dumps({"status": "200", "uid": uid, "message": "Authentication failed"}, ensure_ascii=False,
                           indent=4))
        else:
            # try:
            #     log_data = SwanLog(userID=str(request.user.uuid),
            #                   username=request.user.first_name,
            #                   project_name=business_id.service_name,
            #                   project_uuid=str(business_id.uuid),
            #                   module_name=tgt,
            #                   swan_name=swan_data.swan_name,
            #                   module_args=arg,
            #                   message=u'接口异常',
            #                   status=False,
            #                   update_log=log
            #                   )
            #     print log
            #     print SwanLog.update_log
            #     log_data.save()
            #
            # except:
            #     print "error"
            #     pass
            log_data = SwanLog(userID=str(request.user.uuid),
                              username=request.user.first_name,
                              project_name=business_id.service_name,
                              project_uuid=str(business_id.uuid),
                              module_name=tgt,
                              swan_name=swan_data.swan_name,
                              module_args=arg,
                              message=u'接口异常',
                              status=False,
                              update_log=log
                              )
            log_data.save()
            print log
            return render_to_response('swan/push_error.html', locals(), context_instance=RequestContext(request))

    return HttpResponse(json.dumps({"status": "403", "message": "Authentication failed"}, ensure_ascii=False, indent=4))


@login_required
def swan_select(request):
    """
    异步请求返回当前项目已添加发布按钮
    :param request:
    :return:
    """
    data = {}
    rst_data = []
    user_info = CustomUser.objects.get(first_name=request.user.first_name)

    swan_project_name = request.GET.get("project_name")
    myform_rst = Project.objects.get(pk=swan_project_name)

    rst = project_swan.objects.filter(project_name=myform_rst)
    """
    所有当前项目发布名称放到一个list中
    """

    swan_name_list = [i.swan_name for i in rst]
    if request.user.is_superuser:
        for i in rst:
            data[i.uuid] = i.swan_name

    else:
        swan_push = user_info.project_swan_set.all()
        for i in swan_push:
            if i.swan_name in swan_name_list:
                data[i.uuid] = i.swan_name
    print data
    host_list = myform_rst.host_set.all()
    return render_to_response('swan/select.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_select_myfrom(request):
    """
    异步请求返回当前项目已添加发布按钮
    :param request:
    :return:
    """

    swan_project_name = request.GET.get("project_name")
    myform_rst = Project.objects.get(pk=swan_project_name)
    rst_data = []
    rst = project_swan.objects.filter(project_name=myform_rst)
    data = {}
    for i in rst:
        rst_data.append(i.swan_name)
    host_list = myform_rst.host_set.all()
    host_count = host_list.count()
    business_list = []
    for i in host_list:
        business_list.append({i.eth1: i.business.all()})

    return render_to_response('swan/select_tab.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_select_button(request):
    """
    根据请求返回当前功能所有的机器列表
    :param request:
    :return:
    """
    swan_project_name = request.GET.get("project", False)
    swan_name = request.GET.get("swan_name", False)

    myform_rst = Project.objects.get(uuid=swan_project_name)

    rst_data = []

    rst = project_swan.objects.get(uuid=swan_name, project_name=myform_rst)
    rst_data = rst.node.all()

    host_count = len(rst_data)
    business_list = []
    for i in rst_data:
        business_list.append({i.eth1: i.business.all()})

    return render_to_response('swan/buttom_cmdb.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_select_tgt(request):
    """
    异步请求返回当前项目已添加发布按钮
    :param request:
    :return:
    """
    swan_project_name = request.GET.get("project", False)
    swan_name = request.GET.get("tgt", False)
    type = request.GET.get('type', False)
    myform_rst = Project.objects.get(pk=swan_project_name)
    result = project_swan.objects.get(pk=swan_name)

    rst_data = result.tgt.split()
    if rst_data:
        rst = 'true'

    if type == 'apply':
        return render_to_response('swan/apply_tgt.html', locals(), context_instance=RequestContext(request))
    else:
        return render_to_response('swan/select_tgt.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_apply(request, uuid):
    project_name = Project.objects.all()
    swan_name = project_swan.objects.all()
    try:
        qa_users = department_Mode.objects.get(department_name=u'测试部').users.all()
        op_users = department_Mode.objects.get(department_name=u'运维部').users.all()
    except:
        qa_users = []
        op_user = []
    if request.method == 'POST':
        applyer = CustomUser.objects.get(uuid=uuid)
        project_name = request.POST.get('project_name')
        module_name = request.POST.get('project_all_tag')
        print module_name, project_name
        qa = request.POST.get('qa')
        op = request.POST.get('op')
        comment = request.POST.get('comment')
        if project_swan.objects.get(swan_name=module_name).choose == 0:
            module_type = 0
            module_tgt = request.POST.get('tgt_name')

            a = Apply(applyer=applyer, project_name=project_name, module_name=module_name,
                      qa=qa, op=op, comment=comment, module_type=module_type, module_tgt=module_tgt, status=0)
            a.save()
        else:
            a = Apply(applyer=applyer, project_name=project_name, module_name=module_name,
                      qa=qa, op=op, comment=comment, status=0)
            a.save()
        apply_id = a.id

        qa_mail = CustomUser.objects.get(first_name=qa).email.strip()
        key = token(auth_key=auth_key, id=apply_id, username=applyer, project=project_name, module=module_name)

        url = 'http://%s/swan/apply/p/?id=%s&status=1&key=%s' % (request.get_host(), apply_id, key)
        mail_title = '测试需求'
        mail_msg = """
        Hi,%s:
            有新的发布申请, 详情如下:
                申请人: %s
                申请发布项目: %s
                申请发布功能模块: %s
                申请时间: %s
                发布备注: %s
            请及时测试, 如测试完成, 请点击以下链接, 会交由运维上线。
            %s
        """ % (qa, applyer, project_name, module_name, datetime.datetime.now(), comment, url)

        send_mail(mail_title, mail_msg, 'jkfunshion@fun.tv', [qa_mail], fail_silently=False)
        print qa_mail
        smg = u'申请提交成功!'
        return HttpResponseRedirect('/swan/apply/')

    return render_to_response('swan/apply.html', locals(), context_instance=RequestContext(request))


@login_required
def apply_project(request):
    if request.method == 'GET':
        id = request.GET.get('id')
        status = request.GET.get('status')
        post_key = request.GET.get('key')
        a = Apply.objects.get(id=id)
        b = Apply.objects.filter(id=id)
        applyer, project_name, module_name, qa, op, comment, date_added = \
            a.applyer, a.project_name, a.module_name, a.qa, a.op, a.comment, a.date_added

        qa_mail = CustomUser.objects.get(first_name=qa).email
        op_mail = CustomUser.objects.get(first_name=op).email
        key = token(auth_key, id, applyer, project_name, module_name)

        if key == post_key:
            if status == '1':
                b.update(status='1', date_one=datetime.datetime.now())
                url = 'http://127.0.0.1:9000/swan/apply/exec/?id=%s&key=%s' % (id, key)
                url1 = 'http://127.0.0.1:9000/swan/apply/p/?id=%s&status=2&key=%s' % (id, key)
                mail_title = u'上线申请'
                mail_msg = u"""
                Hi,%s:
                    有新的发布申请, 详情如下:
                        申请人: %s
                        申请发布项目: %s
                        申请发布功能模块: %s
                        申请时间: %s
                        发布备注: %s
                    请及时上线, 上线请点击以下链接。
                    %s
                    上线完成后点击以下链接,告知各位发布完成。
                    %s
                """ % (op, applyer, project_name, module_name, datetime.datetime.now(), comment, url, url1)
                send_mail(mail_title, mail_msg, 'jkfunshion@fun.tv', [op_mail], fail_silently=False)
                smg = u"提交成功,已转交运维上线。"
                return render_to_response('swan/apply.html', locals(), context_instance=RequestContext(request))

            elif status == '2':
                b.update(status='2', date_ended=datetime.datetime.now())
                c = Apply.objects.get(id=id)
                date_one, date_ended = c.date_one, c.date_ended
                mail_title = u'发布完成'
                mail_msg = u"""
                Hi,all:
                    以下发布已完成, 详情如下:
                        申请人: %s
                        申请发布项目: %s
                        申请发布功能模块: %s
                        申请时间: %s
                        发布备注: %s
                        测试完成时间: %s
                        发布完成时间: %s
                """ % (applyer, project_name, module_name, date_added, comment, date_one, date_ended)
                send_mail(mail_title, mail_msg, 'jkfunshion@fun.tv', [qa_mail, op_mail], fail_silently=False)
                smg = u"上线成功,已通知各位。"
                return render_to_response('swan/apply.html', locals(), context_instance=RequestContext(request))


@login_required
def apply_auto(request):
    posts = []
    id = request.GET.get('id')
    post_key = request.GET.get('key')
    if id:
        a = Apply.objects.get(id=id)
        project_name = a.project_name
        module_name = a.module_name
        module_type = a.module_type
        module_tgt = a.module_tgt
        op = a.op

        key = token(auth_key, id, op, project_name, module_name)
        if post_key == key:
            swan = project_swan.objects.get(swan_name=module_name)
            ip, choose = swan.ip, swan.choose
            iplist = ast.literal_eval(ip)
            for ip in iplist:
                posts.append(Host.objects.get(id=ip))

            return render_to_response('swan/apply_exec.html', locals(), context_instance=RequestContext(request))


@login_required
def swan_websocket(request):
    jid = request.GET.get("jid")
    web_socket = websocket_url
    return render_to_response('swan/socket.html', locals(), context_instance=RequestContext(request))


def SwanSelectLog(request, uuid):
    """
    异步请求返回当前项目已添加发布按钮
    :param request:
    :return:
    """
    date = request.GET.get("date")

    day = datetime.datetime.strptime(date, '%Y-%m-%d')
    log_data = SwanLog.objects.filter(project_uuid=uuid, swan_datetime__gte=day).order_by("-swan_datetime")

    return render_to_response('swan/swan_log.html', locals(), context_instance=RequestContext(request))
