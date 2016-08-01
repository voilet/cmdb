#!/usr/bin/env python
#-*- coding: utf-8 -*-
from django import forms

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from django.core.context_processors import csrf
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from models import OperationLog
import time
from accounts.utils import jmmail
from django.template.defaultfilters import linebreaksbr

class OperationLogForm(forms.ModelForm):
    class Meta:
        model = OperationLog
        fields = ['content', 'mail_list', 'mail_title']

@login_required
def log_list(request):
    """
    配置修改记录列表
    """
    context = {}
    log_list = OperationLog.objects.filter().order_by("-id")
    context["log_list"] = log_list
    return render_to_response('config/log_list.html', context, context_instance=RequestContext(request))

# @login_required()
def mail_restart(request, id):
    """
    发送失败邮件列表重新发送
    """
    content = {}
    log_id = OperationLog.objects.get(id=id)
    OperationLog_save = OperationLog(id=log_id.id, user_id=log_id.user_id, content=log_id.content, date_created=log_id.date_created, mail_list=log_id.mail_list, mail_status=True, mail_title=log_id.mail_title)
    OperationLog_save.save()
    content["status"] = True
    return render_to_response("config/mail_ok.html", locals())


@login_required
@csrf_protect
def new_log(request):
    context = {}
    if request.method == "POST":
        post_data = request.POST
        form = OperationLogForm(post_data)
        if form.is_valid(): 
            log = form.save(commit=False)
            log.user = request.user

            log.save()
            return HttpResponseRedirect("/conf/log_list/")
    else:
        form = OperationLogForm()
        context['form'] = form
        context.update(csrf(request))
    return render_to_response('config/log_new.html', locals(), context_instance=RequestContext(request))
