#!/usr/bin/python
# -*-coding:utf-8-*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from accounts.models import UserCreateForm
from django.http import HttpResponse, HttpResponseRedirect
from users.models import department_Mode
from users.models import CustomUser
from django import forms
from cmdb_auth.no_auth import check_auth
import json
import hashlib
import time
from mysite.settings import auth_key, EMAIL_PUSH
from django.core.mail import send_mail
from forms import AuthNodeForm
import uuid
import random
from users.models import cmdb_uuid


def register(request):
    status = check_auth(request, "add_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    content = {}
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.is_staff = 1
            new_user = form.save(commit=False)

            new_user.is_staff = 1
            new_user.session_key = ""
            new_user.uuid = cmdb_uuid()
            new_user.save()
            if EMAIL_PUSH:
                token = str(hashlib.sha1(new_user.username + auth_key + new_user.uuid +
                                         time.strftime('%Y-%m-%d', time.localtime(time.time()))).hexdigest())
                #
                url = u'http://%s/accounts/newpasswd/?uuid=%s&token=%s' % (request.get_host(), new_user.uuid, token)
                mail_title = u'运维自动化初始密码'
                mail_msg = u"""
                Hi,%s:
                    请点击以下链接初始化运维自动化密码,此链接当天有效:
                        %s
                    有任何问题，请随时和运维组联系。
                """ % (new_user.first_name, url)
                #

                send_mail(mail_title, mail_msg, u'运维自动化<devops@funshion.net>', [new_user.email], fail_silently=False)

            return HttpResponseRedirect('/accounts/user_list/')
        else:
            data = UserCreateForm()

            return render_to_response('user/reg.html', locals(), context_instance=RequestContext(request))
    else:
        data = UserCreateForm()
        return render_to_response('user/reg.html', locals(), context_instance=RequestContext(request))


class department_from(forms.ModelForm):
    class Meta:
        model = department_Mode
        fields = "__all__"


@login_required
def user_select(request):
    u"""
    查看用户
    """
    status = check_auth(request, "add_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    uf = CustomUser.objects.all().filter(is_active=True, is_staff=True)

    return render_to_response('user/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def user_old(request):
    u"""
    离职用户
    """
    status = check_auth(request, "add_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    uf = CustomUser.objects.all().filter(is_active=False, is_staff=False)

    return render_to_response('user/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def user_list_status(request):
    u"""
    离职用户
    """
    status = check_auth(request, "add_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    uf = CustomUser.objects.all().filter(is_active=True, is_staff=False)

    return render_to_response('user/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def user_status(request, id):
    u"""
    查看用户
    """
    status = check_auth(request, "delete_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    user = CustomUser.objects.get(pk=id)
    if user.is_staff:
        user.is_staff = False
    else:
        user.is_staff = True
    user.save()
    return render_to_response('user/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def user_delete(request, id):
    u"""
    查看用户
    """
    status = check_auth(request, "delete_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    user = CustomUser.objects.get(pk=id)
    user.is_staff = False
    user.is_active = False
    user.save()

    return render_to_response('user/user_list.html', locals(), context_instance=RequestContext(request))


@login_required
def department_view(request):
    u"""
    添加部门
    """
    status = check_auth(request, "add_department")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    #验证post方法
    if request.method == 'POST':
        uf = department_from(request.POST)

        if uf.is_valid():
            uf.save()
        # return render_to_response('user/department_add.html', locals(), context_instance=RequestContext(request))
        return HttpResponseRedirect("/accounts/list_department/")
    else:
        uf = department_from()
    return render_to_response('user/add_usergroup.html', locals(), context_instance=RequestContext(request))


@login_required
def department_edit(request, id):
    u"""
    部门修改
    """
    status = check_auth(request, "add_department")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    data = department_Mode.objects.get(id=id)
    if request.method == 'POST':
        uf = department_from(request.POST, instance=data)
        u"验证数据有效性"
        if uf.is_valid():
            uf.save()
        return HttpResponseRedirect("/accounts/list_department/")

    uf = department_from(instance=data)
    return render_to_response('user/bootstorm_from.html', locals(), context_instance=RequestContext(request))


@login_required
def department_list(request):
    u"""
    添加部门
    """
    status = check_auth(request, "add_department")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    uf = department_Mode.objects.all()

    content = {}

    for i in uf:
        user_list = []
        dep_all = i.users.all().values("first_name")

        for t in dep_all:
            user_list.append(t.get("first_name"))
        content[i.department_name] = {"user_list": user_list, "department_id": i.id}

    return render_to_response('user/department_list.html', locals(), context_instance=RequestContext(request))


def logout_view(request):
    u"""
    退出登录
    """
    # auth.logout(request)
    request.session.flush()
    return HttpResponseRedirect("/")


def menu_class(request):
    user = request.user.username
    try:
        menu = CustomUser.objects.get(username=user)
        if menu.menu_status:
            menu.menu_status = False
            menu.save()
        else:
            menu.menu_status = True
            menu.save()

        content = {"status": 200, "message": "update is ok"}
    except:
        content = {"status": 403, "message": "what ary you doing"}
    return HttpResponse(json.dumps(content, ensure_ascii=False, indent=4, ))


@login_required
def user_auth_node(request):
    u"""
    查看用户
    """
    data = AuthNodeForm()

    return render_to_response('default/test.html', locals(), context_instance=RequestContext(request))
