#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_protect
from users.models import CustomUser

from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch
from assets.models import Project, System_usage, Service, Line, ProjectUser
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from assets.models import ENVIRONMENT
from users.models import server_auth, department_Mode
from assets.models import project_swan
from cmdb_auth.no_auth import check_auth
from cmdb_auth.models import AuthNode
from assets.zabbix import zabbix_group_add, zabbix_group_del
from mysite.settings import zabbix_on
from accounts.forms import AuthNodeForm

import time
import ast


class business_form(forms.ModelForm):
    # FAVORITE_COLORS_CHOICES = CustomUser.objects.values_list("id", "first_name",)
    # service_user = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)
    # Service_checkbox = Service.objects.values_list("id", "name",)
    # service = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=Service_checkbox)
    try:
        dev_group = department_Mode.objects.get(desc_gid=1003)
        FAVORITE_COLORS_CHOICES = CustomUser.objects.values_list("id", "first_name").filter(department_id=dev_group.id)
        # FAVORITE_COLORS_CHOICES = CustomUser.objects.values_list("id", "first_name")
        project_user_group = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple,
                                                       choices=FAVORITE_COLORS_CHOICES, label=u"用户列表")
    # project_user_group = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES, label=u"用户列表")
    except:
        pass

    class Meta:
        model = Project
        fields = ["service_name",
                  # "service_user",
                  "aliases_name",
                  "project_contact",
                  "project_contact_backup",
                  "description",
                  "line",
                  "project_user_group",
                  "sort",
                  ]

    def save(self, commit=False):
        instance = super(business_form, self).save(commit=True)
        # service_ids = self.cleaned_data.get('service')
        # service_list = Service.objects.filter(id__in=service_ids)
        # for one in service_list:
        #     _, o = ServiceMyForm.objects.get_or_create(business=instance, service=one)
        instance.save()
        return instance


def business_item_ajax(request):
    id = request.GET.get('id')
    s = Project.objects.get(pk=id)
    item = get_object_or_404(Project, pk=id)
    server_list = item.host_set
    # t = get_object_or_404(ProjectUser, myform = item, user = request.user)#check permissions
    all_env = ENVIRONMENT
    host_list = Host.objects.filter(business=item)
    env = request.GET.get("env", None)
    swan_list = project_swan.objects.filter(project_name=item.id)
    return render_to_response('assets/business_item_widget.html', locals(),
                              context_instance=RequestContext(request))


@login_required()
def business_host_list(request, uuid):
    """
    项目主机列表
    """
    context = {}
    item = get_object_or_404(Project, uuid=uuid)
    # 此处权限还需在验证，直接返回 404对异步操作体验很不友好
    # //t = get_object_or_404(ProjectUser, myform=item, user=request.user)   # check permissions
    business_item = Project.objects.get(uuid=uuid)
    form_user = ProjectUser.objects.filter(project=business_item)

    form_user = [one.user for one in form_user]
    user = CustomUser.objects.get(pk=request.user.id)

    if request.user not in form_user:
        return render_to_response('saltstack/server_type_node_error.html', locals(),
                                  context_instance=RequestContext(request))

    all_env = ENVIRONMENT
    env = request.GET.get("env", None)
    form_user_auth = ProjectUser.objects.get(project=business_item, user=user)
    user_env = ast.literal_eval(form_user_auth.env)

    if env:
        if env == "all":
            host_list = business_item.host_set.all()
        else:
            host_list = business_item.host_set.filter(env=env)
        return render_to_response('assets/host_list_widget.html', locals(), context_instance=RequestContext(request))
    return render_to_response('saltstack/server_type_node.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def server_type_item(request):
    service_name = request.GET.get("service_name")
    business_name = Project.objects.get(service_name=service_name)
    server_list = business_name.host_set.all()
    server_list_count = server_list.count()

    centos = business_name.host_set.filter(system="CentOS").count()

    business_list = []
    for i in server_list:
        business_list.append({i.eth1: i.business.all()})

    return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))


@login_required
def server_type_auth(request):
    """
    权限分配，不同用户不同权限
    """
    if not request.user.is_superuser:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    id = request.GET.get('id')
    auth_id = request.GET.get('auth_id')
    business_name = Project.objects.get(pk=id)

    user_data = CustomUser.objects.get(pk=auth_id)
    server_list = Host.objects.filter(business=business_name)
    ip_list = []
    data = AuthNode.objects.filter(project=str(business_name.uuid), user_name=user_data.id)
    rst = data.count()
    if rst:
        for i in data:
            ip_list.append(i.node.uuid)
    return render_to_response('assets/auth_type.html', locals(), context_instance=RequestContext(request))


def project_doc(request, uuid):
    """
    业务维护文档调用
    """
    item = Project.objects.get(uuid=uuid)
    return render_to_response('assets/server_type_doc.html', locals(),
                              context_instance=RequestContext(request))


def project_doc_edit(request, uuid):
    item = Project.objects.get(uuid=uuid)
    uf = project_doc_form(instance=item)
    if request.method == 'POST':
        uf = project_doc_form(request.POST, instance=item)
        if uf.is_valid():
            zw = uf.save(commit=False)
            zw.id = id
            zw.project_doc = request.POST.get("project_doc")
            zw.save()
        return render_to_response('assets/server_type_doc.html', locals(), context_instance=RequestContext(request))
    return render_to_response('assets/server_type_doc_edit.html', locals(), context_instance=RequestContext(request))


class MyFormUser_Form(forms.ModelForm):
    class Meta:
        model = ProjectUser
        fields = "__all__"


@login_required
@csrf_protect
def auth_server_type_user_select(request, uuid):
    """
    manage Project's user
    """

    business_item = Project.objects.get(uuid=uuid)
    user = request.user
    if not request.user.is_superuser:
        return render_to_response('auth/auth_jquery.html', locals(), context_instance=RequestContext(request))

    user_all = CustomUser.objects.all()
    form_user = ProjectUser.objects.filter(project=business_item)
    form_one_user = [one.user for one in form_user]
    user_test = [one.env for one in form_user]
    rest_user = [one for one in user_all if one not in form_one_user]
    # rest_user = [one for one in user_all if one not in form_one_user and not one.is_superuser]

    return render_to_response('assets/server_type_user_edit.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def auth_server_type_user_add(request, uuid):
    """
    add Project's user
    """

    user_id = request.GET.get("user_id", '-1')
    user = get_object_or_404(CustomUser, pk=user_id)
    business_item = Project.objects.get(uuid=uuid)
    user_all = CustomUser.objects.all()
    form_user = ProjectUser.objects.filter(project=business_item)
    env = ["st", "dev", "prod", "publish"]
    user_from = MyFormUser_Form()

    # if 'admin' not in request.user.department:
    #         return HttpResponse("没有权限")

    if request.method == 'POST':
        user_id = request.POST.get("user_id", '-1')
        user = get_object_or_404(CustomUser, pk=user_id)
        business_item = Project.objects.get(uuid=uuid)
        env = request.POST.getlist("env")
        # try:
        #     s = ProjectUser.objects.get(user=user)
        #     s.env = repr(env)
        #     s.save()
        #     # a = ProjectUser.objects.select_for_update(env=repr(env)).filter(user=s)
        # except ProjectUser.DoesNotExist:
        #     a = ProjectUser.objects.get_or_create(user=user, myform=business_item, env=repr(env))
        a = ProjectUser.objects.get_or_create(user=user, project=business_item, env=repr(env))

        business_item = Project.objects.get(uuid=uuid)
        user = request.user

        form_one_user = [one.user for one in form_user]
        rest_user = [one for one in user_all if one not in form_one_user and not one.is_superuser]

        return render_to_response('assets/server_type_user_edit.html', locals(),
                                  context_instance=RequestContext(request))

    form_user = [one.user for one in form_user]
    # rest_user = [one for one in user_all if one not in form_user and not one.is_superuser]
    rest_user = [one for one in user_all if one not in form_user]

    try:
        form_user_id = ProjectUser.objects.get(project=business_item, user=user)
        env_in = form_user_id.env
        if env_in:
            env_in = ast.literal_eval(env_in)
        else:
            env_in = []
        form_user_status = True
    except ProjectUser.DoesNotExist:
        form_user_status = False

    return render_to_response('assets/server_type_user_add.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def auth_server_type_user_edit(request, id):
    """
    edit Project's user
    """

    user_id = request.GET.get("user_id", '-1')
    user = get_object_or_404(CustomUser, pk=user_id)
    business_item = Project.objects.get(id=id)
    user_all = CustomUser.objects.all()
    form_user = ProjectUser.objects.filter(myform=business_item)
    env = ["st", "dev", "prod", "publish"]
    user_from = MyFormUser_Form()

    # if 'admin' not in request.user.department:
    #         return HttpResponse("没有权限")

    if request.method == 'POST':
        user_id = request.POST.get("user_id", '-1')
        user = get_object_or_404(CustomUser, pk=user_id)
        business_item = Project.objects.get(id=id)
        env = request.POST.getlist("env")

        s = ProjectUser.objects.get(myform=business_item, user=user)
        s.env = repr(env)
        s.save()

        business_item = Project.objects.get(id=id)
        # user = request.user

        form_one_user = [one.user for one in form_user]
        rest_user = [one for one in user_all if one not in form_one_user and not one.is_superuser]

        return render_to_response('assets/server_type_user_edit.html', locals(),
                                  context_instance=RequestContext(request))

    form_user = [one.user for one in form_user]
    rest_user = [one for one in user_all if one not in form_user and not one.is_superuser]

    try:
        form_user_id = ProjectUser.objects.get(myform=business_item, user=user)
        env_in = form_user_id.env
        if env_in:
            env_in = ast.literal_eval(env_in)
        else:
            env_in = []
        form_user_status = True
    except ProjectUser.DoesNotExist:
        form_user_status = False
    except ProjectUser.MultipleObjectsReturned:
        form_user_status = False

    return render_to_response('assets/server_project_user_edit.html', locals(),
                              context_instance=RequestContext(request))


@login_required
@csrf_protect
def auth_server_type_user_delete(request, id):
    """
    delete Project's user
    """
    user_id = request.GET.get("user_id", '-1')
    user = get_object_or_404(CustomUser, pk=user_id)
    business_item = Project.objects.get(id=id)
    form_user = ProjectUser.objects.filter(user=user, myform=business_item)
    form_user.delete()

    user_all = CustomUser.objects.all()
    form_user = ProjectUser.objects.filter(myform=business_item)
    form_one_user = [one.user for one in form_user]
    user_test = [one.env for one in form_user]
    rest_user = [one for one in user_all if one not in form_one_user and not one.is_superuser]

    return render_to_response('assets/server_type_user_edit.html', locals(), context_instance=RequestContext(request))


# 业务管理
@login_required
@csrf_protect
def server_type_add(request):
    """
    添加项目方法，用于主机业目分配
    """
    status = check_auth(request, "add_project")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    if request.method == 'POST':  # 验证post方法
        uf = business_form(request.POST)  # 绑定POST动作
        init = request.GET.get("init", False)
        if uf.is_valid():
            uf.save()
            project_name = uf.cleaned_data['service_name']
            if zabbix_on:
                ret = zabbix_group_add(project_name)
                if ret == 0:
                    pass
            if not init:
                return HttpResponseRedirect("/assets/server/type/list/")
            else:
                return HttpResponseRedirect("/assets/host_add/")
    else:
        uf = business_form()
        try:
            dev_group = department_Mode.objects.get(desc_gid=1003)
            user_list = CustomUser.objects.filter(department_id=dev_group.id)
        except:
            pass
        user_group = []
        # user_list = CustomUser.objects.filter(is_superuser__isnull=True)

    return render_to_response('assets/server_type_add.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def auth_server_type_edit(request, uuid):
    """
    业务修改模块
    """
    status = check_auth(request, "edit_project")
    if not status:
        return render_to_response('auth/auth_jquery.html', locals(), context_instance=RequestContext(request))

    server_type = Project.objects.all()
    business_name = Project.objects.get(uuid=uuid)
    form_user_qs = ProjectUser.objects.filter(project=business_name)
    form_user = [one.user for one in form_user_qs]
    uf = business_form(instance=business_name)

    try:
        dev_group = department_Mode.objects.get(desc_gid=1003)
        dev_group_userlist = CustomUser.objects.filter(department_id=dev_group.id)
    except:
        pass

    if business_name.project_user_group:
        user_list_id = [int(i) for i in ast.literal_eval(business_name.project_user_group)]

    if request.method == 'POST':
        print "*" * 100
        print request.POST.getlist("project_user_group")
        uf = business_form(request.POST, instance=business_name)
        print uf
        if uf.is_valid():
            myform = uf.save()
            return render_to_response('assets/server_type_edit_ok.html', locals(),
                                      context_instance=RequestContext(request))

    return render_to_response('assets/server_type_edit.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def auth_server_type_del(request, uuid):
    """
    业务删除
    """
    status = check_auth(request, "delete_project")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    if Project.objects.filter(uuid=uuid).count() > 0:
        business_item = Project.objects.get(uuid=uuid)
        project_swan.objects.filter(project_name_id=business_item.uuid).delete()
        # idc_log(request.user.username, business_item.service_name, "业务删除", request.user.username, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), id, request.user.id)
        business_item.delete()  # 这个删除会删除该业务下的机器
        project_name = business_item.service_name
        ret = zabbix_group_del(project_name)
        if ret == 0:
            pass
    return HttpResponseRedirect("/assets/server/type/list/")


# 业务维护文档
class project_doc_form(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["project_doc"]


# 业务管理
@login_required
def auth_server_type_list(request):
    business_list = Project.objects.all()
    return render_to_response('assets/server_type_list.html', locals(), context_instance=RequestContext(request))


# 业务管理
@login_required
def auth_server_type_list(request):
    status = check_auth(request, "project_auth")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    business_list = Project.objects.all()

    server_type = Project.objects.all()

    service_user = ProjectUser.objects.filter()
    swan_all = project_swan.objects.all()
    return render_to_response('assets/server_type_list.html', locals(), context_instance=RequestContext(request))
