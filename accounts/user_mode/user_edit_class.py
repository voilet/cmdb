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
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from accounts.models import UserCreateForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.hashers import make_password
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from accounts.models import *
from users.models import department_Mode
import time,json
from django.contrib.auth.decorators import login_required
from cmdb_auth.no_auth import check_auth



class edit_user_from(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = "__all__"

@login_required
@csrf_protect
def user_id(request, id):
    voilet_list = CustomUser.objects.get(id=id)
    content = {}
    data_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if request.method == 'POST':
        if request.POST.getlist("password1") == request.POST.getlist("password2"):
            uf = edit_user_from(request.POST)
            if uf.is_valid():
                # print "is ok"
                zw = uf.save(commit=False)
                zw.last_login = data_time
                zw.date_joined = data_time
                zw.id = id
                zw.password = make_password(request.POST.getlist("password1"))
                zw.save()
                content["user_list"] = voilet_list
                content.update(csrf(request))
                return render_to_response('user/user_edit.html', content, context_instance=RequestContext(request))
            # else:
            #     print "is over"
    else:
        content["data_time"] = data_time
        content["user_list"] = voilet_list
        content["department"] = department_Mode.objects.all()
        content["jobs_name"] = manager_demo
        content.update(csrf(request))
        return render_to_response('user/user_page.html', content, context_instance=RequestContext(request))

class department_from(forms.ModelForm):
    class Meta:
        model = department_Mode
        fields = "__all__"

class useredit_from(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "email", "mobile", "department", "user_key"]


@login_required
@csrf_protect
def user_edit(request, id):
    status = check_auth(request, "edit_user")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    data = CustomUser.objects.get(id=id)
    data_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    if request.method == 'POST':
        # if request.POST.getlist("password1") == request.POST.getlist("password2"):
        uf = useredit_from(request.POST, instance=data)
        # print uf
        if uf.is_valid():
            # zw = uf.save(commit=False)
            # zw.last_login = data_time
            # zw.date_joined = data_time
            # zw.username = data.username
            # zw.id = id
            uf.save()
            return HttpResponseRedirect("/accounts/user_list/")
    else:
        uf = useredit_from(instance=data)
        return render_to_response('user/user_edit.html', locals(), context_instance=RequestContext(request))

class userupdate_from(forms.ModelForm):
    # password1 =  models.CharField(max_length=64, verbose_name=u'确认密码')

    class Meta:
        model = CustomUser
        fields = ["first_name", "password", "email", "mobile", "user_key"]


@login_required
def user_update(request):
    data = CustomUser.objects.get(username=request.user.username)
    data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if request.method == 'POST':
        uf = userupdate_from(request.POST, instance=data)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect("/accounts/user_list/")
    else:
        uf = userupdate_from(instance=data)
        return render_to_response('user/user_edit.html', locals(), context_instance=RequestContext(request))

