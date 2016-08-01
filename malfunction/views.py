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
# 登录
from users.models import CustomUser
from models import Incident
from froms import inclident_from, zabbix_from, script_from, smokeping_from, Editinclident_from
from django.views.decorators.csrf import csrf_exempt
from assets.models import Host
import time
from django.core.mail import send_mail
from mysite.settings import ops_mail, website, SendMail
import datetime
from users.models import department_Mode, CustomUser


@login_required
def FaultIndex(request):
    data = Incident.objects.all().order_by("-createtime")
    return render_to_response('malfunction/index.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultMy(request):
    """
    我的故障
    """
    data = Incident.objects.filter(projectuser=request.user.first_name, status__gte=1).order_by("-createtime")
    return render_to_response('malfunction/my.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultClassical(request):
    """
    精典案例
    """
    data = Incident.objects.filter(classical=True).order_by("-createtime")
    return render_to_response('malfunction/classical.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultDetail(request, uuid):
    """
    详情页
    """
    uuid = str(uuid)
    data = Incident.objects.get(uuid=uuid)
    if data.stoptime and data.starttime:
        sum_time = data.stoptime - data.starttime
    grade_status = data.get_grade_display()
    print data.get_grade_display()
    return render_to_response('malfunction/detail.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultEdit(request, uuid):
    """
    修改
    """
    uuid = str(uuid)
    faul_data = Incident.objects.get(uuid=uuid)

    if request.method == "POST":
        close_user = request.POST.get("status")
        uf = Editinclident_from(request.POST, instance=faul_data)
        if uf.is_valid():
            zw = uf.save(commit=False)
            if int(close_user) == 1:
                zw.closeuser = request.user.first_name
            if not request.POST.get("stoptime"):
                zw.stoptime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            zw.save()
            mail_title = zw.title
            mailcomment = str(zw.mailcomment).replace("/upload/", website + "/upload/")
            content = str(zw.comment).replace("/upload/", website + "/upload/")
            mail_msg = """<!DOCTYPE html>
            <html>
            <head>
                <head data-suburl="">
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
                <meta name="author" content="运维管理系统" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>运维自动化平台</title>
                <!-- 新 Bootstrap 核心 CSS 文件 -->
                <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">

                <!-- 可选的Bootstrap主题文件（一般不用引入） -->
                <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

                <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
                <script src="http://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
                <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
                <script src="http://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
            </head>

            <body>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-12">
                        <div>
                            <h2>故障详情如下:</h2>
                            <p>报障人员: %s</p>
                            <p>报警内容: %s</p>
                            <p>处理状态: %s</p>
                            <p>发生时间: %s</p>
                            <p>发现时间: %s</p>
                            <p>解决时间: %s</p>
                            <p>解决过程: %s</p>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="alert alert-success alert-dismissable">
                            <h4>提醒!</h4>
                            此邮件为系统自动发送,请勿回复
                        </div>
                        <p>关注运维团队微信,可接收微信报警通知</p>
                    </div>
                </div>
            </div>
            </body></html>""" % (zw.incident_user, mailcomment, zw.get_status_display(),  zw.starttime, zw.scantime, zw.stoptime,  content)
            mail_list = []
            mail_list.append(ops_mail)
            if faul_data.project_principal:
                mail_list.append(faul_data.project_principal)
            send_mail("Re: %s" % mail_title, "", SendMail, mail_list, fail_silently=False,
                      html_message=mail_msg)

        return HttpResponseRedirect('/incident/' + uuid + "/")

    data = inclident_from(instance=faul_data)
    status = faul_data.status
    classical = faul_data.classical

    return render_to_response('malfunction/edit.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultDone(request):
    """
    done 故障
    """
    data = Incident.objects.filter(status=2).order_by("-createtime")
    return render_to_response('malfunction/done.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultSource(request):
    """
    done 故障
    """
    name = request.GET.get("name", False)
    if name:
        data = Incident.objects.filter(source=name).order_by("-createtime")
        return render_to_response('malfunction/index.html', locals(), context_instance=RequestContext(request))
    return HttpResponseRedirect('/incident/')


@login_required
def FaultNoDone(request):
    """
    done 故障
    """
    data = Incident.objects.filter(status__lte=1).order_by("-createtime")
    return render_to_response('malfunction/nodone.html', locals(), context_instance=RequestContext(request))


@login_required
def FaultAdd(request):
    data = inclident_from()
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    if request.method == "POST":
        uf = inclident_from(request.POST)
        close_user = request.POST.get("status", False)
        if uf.is_valid():
            zw = uf.save(commit=False)
            if close_user:
                zw.closeuser = request.user.first_name
            zw.incident_user = request.user.first_name
            zw.save()
            mail_title = zw.title
            mailcomment = str(zw.mailcomment).replace("/upload/", website + "/upload/")
            content = str(zw.comment).replace("/upload/", website + "/upload/")
            mail_msg = """<!DOCTYPE html>
            <html>
            <head>
                <head data-suburl="">
                <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
                <meta http-equiv="X-UA-Compatible" content="IE=edge"/>
                <meta name="author" content="运维管理系统" />
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>运维自动化平台</title>
                <!-- 新 Bootstrap 核心 CSS 文件 -->
                <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap.min.css">

                <!-- 可选的Bootstrap主题文件（一般不用引入） -->
                <link rel="stylesheet" href="http://cdn.bootcss.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">

                <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
                <script src="http://cdn.bootcss.com/jquery/1.11.3/jquery.min.js"></script>
                <!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
                <script src="http://cdn.bootcss.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
            </head>

            <body>
            <div class="container-fluid">
                <div class="row">
                    <div class="col-md-12">
                        <div>
                            <h2>故障详情如下:</h2>
                            <p>报障人员: %s</p>
                            <p>报警内容: %s</p>
                            <p>处理状态: %s</p>
                            <p>发生时间: %s</p>
                            <p>发现时间: %s</p>
                            <p>解决时间: %s</p>
                            <p>解决过程: %s</p>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="alert alert-success alert-dismissable">
                            <h4>提醒!</h4>
                            此邮件为系统自动发送,请勿回复
                        </div>
                        <p>关注运维团队微信,可接收微信报警通知</p>
                    </div>
                </div>
            </div>
            </body></html>""" % (zw.incident_user, mailcomment, zw.get_status_display(), zw.starttime, zw.scantime, zw.stoptime, content)

            mail_list = []
            mail_list.append(ops_mail)
            if zw.project_principal:
                mail_list.append(zw.project_principal)
            send_mail(mail_title, "", SendMail, mail_list, fail_silently=False, html_message=mail_msg)

            return HttpResponseRedirect('/incident/' + str(zw.uuid) + "/")
    return render_to_response('malfunction/add.html', locals(), context_instance=RequestContext(request))


@csrf_exempt
def FaultApi(request):
    """
    监控及脚本探测api
    :param request:
    :return:
    """
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if request.method == "POST":
        source = request.GET.get("source", False)
        if source:
            if source == "zabbix" or source == "nagios" or source == "cacti":
                data = zabbix_from(request.POST)
                if data.is_valid():
                    zw = data.save(commit=False)
                    zw.source = source
                    zw.starttime = date_time
                    zw.scantime = date_time
                    zw.save()
                    content = {"status": 200, "msg": u"ok"}
                    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))

            if source == "smokeping":
                data = smokeping_from(request.POST)
                print data
                if data.is_valid():
                    zw = data.save(commit=False)
                    zw.source = source
                    zw.starttime = date_time
                    zw.scantime = date_time
                    zw.save()
                    content = {"status": 200, "msg": u"ok"}
                    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))

            if source == u'监控脚本':
                data = script_from(request.POST)
                if data.is_valid():
                    zw = data.save(commit=False)
                    zw.source = source
                    zw.starttime = date_time
                    zw.scantime = date_time
                    zw.save()
                    content = {"status": 200, "msg": u"ok"}
                return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))

        content = {"status": 403, "msg": u"参数不完整"}
        return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4))

    content = {"status": 403, "msg": u"禁止get提交"}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4), content_type="application/json")
