#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: project_conf.py
# Desc: 2014-14/12/31:上午11:38
# Author: 苦咖啡
# Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.template import RequestContext
from assets.models import Project, Host
from assets.models import project_swan, swan_pro, swan_port
from django import forms
import ast
from django.contrib.auth.decorators import login_required
from config.forms import *
from config.forms import *


# @csrf_exempt

@login_required()
def Code_add(request):
    """

    :param request:
    :return:
    """
    uf = CodeForm()
    if request.method == 'POST':
        uf = CodeForm(request.POST)
        if uf.is_valid():
            zw = uf.save(commit=False)
            zw.save()

    return render_to_response('swan/add_code_templates.html', locals(), context_instance=RequestContext(request))


@login_required()
def project_add(request, uuid):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))
    uf = ProjectForm(business=item.uuid)
    if request.method == 'POST':
        uf = ProjectForm(request.POST, business=item)
        if uf.is_valid():
            zw = uf.save(commit=False)
            zw.project_name = item
            zw.choose = 0
            zw.save()
            uf.save_m2m()
            print "save ok"
        return HttpResponseRedirect("/assets/server/type/list/")

    return render_to_response('config/swan_default.html', locals(), context_instance=RequestContext(request))


@login_required()
def project_config(request, uuid):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))

    uf = swan_all_form(business=item.uuid)
    if request.method == 'POST':
        uf = swan_all_form(request.POST, business=item.uuid)
        if uf.is_valid():
            zw = uf.save(commit=False)

            zw.project_name = item
            zw.save()
            uf.save_m2m()

            return HttpResponseRedirect("/assets/server/type/list/")
    return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))


@login_required()
def project_git(request, uuid):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))
    uf = GitCodeForm(business=item)
    if request.method == 'POST':
        uf = GitCodeForm(request.POST, business=item)
        if uf.is_valid():
            zw = uf.save(commit=False)

            zw.project_name = item
            zw.choose = 2
            zw.save()
            uf.save_m2m()

            return HttpResponseRedirect("/assets/server/type/list/")
    return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))


@login_required()
def projectJava(request, uuid):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))
    uf = JavaCodeForm(business=item)
    if request.method == 'POST':
        uf = JavaCodeForm(request.POST, business=item)
        if uf.is_valid():
            zw = uf.save(commit=False)

            zw.project_name = item
            zw.choose = 3
            zw.save()
            uf.save_m2m()

            return HttpResponseRedirect("/assets/server/type/list/")
    return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))


@login_required()
def project_shell(request, uuid):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))
    uf = ShellCodeForm(business=item)
    if request.method == 'POST':
        uf = ShellCodeForm(request.POST, business=item)
        print uf
        if uf.is_valid():
            zw = uf.save(commit=False)

            zw.project_name = item
            zw.choose = 4
            zw.save()
            uf.save_m2m()
            return HttpResponseRedirect("/assets/server/type/list/")
    return render_to_response('config/bootstrap.html', locals(), context_instance=RequestContext(request))


# @csrf_exempt
def project_edit(request, uuid, id):
    """
    :param request:
    :return:
    """
    item = Project.objects.get(uuid=str(uuid))
    swan_data = project_swan.objects.get(uuid=id)
    data = swan_data.node.all()
    ip_list = [x.uuid for x in data]
    host_list = Host.objects.filter(business=item)
    choose = int(swan_data.choose)
    if request.method == 'POST':
        if choose == 2:
            data = GitEditCodeForm(request.POST, business=item.uuid, instance=swan_data)

        elif choose == 3:
            data = JavaCodeForm(request.POST, business=item.uuid, instance=swan_data)

        else:
            data = ShellCodeForm(request.POST, business=item.uuid, instance=swan_data)
        if data.is_valid():
            data.save()

            return HttpResponseRedirect("/assets/server/type/list/")
    if choose == 2:
        uf = GitCodeForm(business=item.uuid, instance=swan_data)

    elif choose == 3:
        uf = JavaCodeForm(business=item.uuid, instance=swan_data)

    else:
        uf = ShellCodeForm(business=item.uuid, instance=swan_data)

    return render_to_response('swan/edit_swan_git.html', locals(), context_instance=RequestContext(request))

        # return render_to_response('swan/edit_swan.html', locals(), context_instance=RequestContext(request))
