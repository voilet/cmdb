#!/usr/bin/python
#-*-coding:utf-8-*-

from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from forms import LoginForm, ChangePasswordForm
import json
from django.views.decorators.csrf import csrf_exempt
from cmdb_auth.models import auth_group, user_auth_cmdb
from accounts.auth_session import auth_class
from users.models import CustomUser
from django.contrib.auth.hashers import make_password, check_password
import hashlib
import time
from mysite.settings import auth_key
from django.contrib.auth import login
from .forms import NewPasswordForm, ResetPasswordForm
from django.core.mail import send_mail
from validators import Checkpasswd


def user_login(request):
    """
    select,    edit    update    delete
    project_nam
    add_user    edit_user    edit_pass    delete_user
    :param request:
    :return:
    """
    if request.method == "POST":
        # form = LoginForm(request=request, data=request.POST)
        # if form.is_valid():
        #     auth_data = auth_class(request.user)
        #     request.session["fun_auth"] = auth_data
        #     user_data = CustomUser.objects.get(first_name=request.user)
        #     user_data.session_key = request.session.session_key
        #     user_data.save()
        #     return HttpResponseRedirect('/')
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            try:
                data = CustomUser.objects.get(username=username)
                check_data = check_password(password, data.password)
                if check_data:
                    data.backend = 'django.contrib.auth.backends.ModelBackend'
                    login(request, data)
                    auth_data = auth_class(request.user)
                    request.session["fun_auth"] = auth_data
                    user_data = CustomUser.objects.get(email=request.user)
                    user_data.session_key = request.session.session_key
                    user_data.save()
                    request.session.set_expiry(28800)
                    return HttpResponseRedirect(request.GET['next'])
            except:
                return render_to_response('user/login.html', locals(), context_instance=RequestContext(request))

    return render_to_response('user/login.html', locals(), context_instance=RequestContext(request))


@login_required
def change_password(request):
    if request.method == "POST":
        form = ChangePasswordForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            ret = {"status": 1, "msg": "is ok"}
        else:
            ret = {"status": 0, "msg": "is over"}
        obj = json.dumps(ret)
        return HttpResponse(obj)
    else:
        obj = json.dumps({"status": -1, "msg": "error"})
        return HttpResponse(obj)


def new_password(request):
    uuid = request.GET.get("uuid", False)
    token = request.GET.get('token', False)

    # try:
    data = CustomUser.objects.get(uuid=uuid)
    new_token = str(hashlib.sha1(data.username + auth_key + data.uuid +
                                     time.strftime('%Y-%m-%d', time.localtime(time.time()))).hexdigest())
    uf = NewPasswordForm()
    if token == new_token:
        if request.method == 'POST':
            uf = NewPasswordForm(request.POST, instance=data)
            if uf.is_valid():
                rst = Checkpasswd(request.POST.get("newpassword"))
                if rst:
                    password = request.POST.get("newpassword")
                    zw = uf.save(commit=False)
                    zw.password = make_password(password, None, 'pbkdf2_sha256')
                    zw.save()
                    status = True
                    return HttpResponseRedirect('/')
                else:
                    status = False
        status = True
        return render_to_response('user/bootstorm.html', locals(), context_instance=RequestContext(request))
    # except:
    #     print "error"
    #     pass
    return render_to_response('404.html', locals(), context_instance=RequestContext(request))


def Resetpassword(request):
    uf = ResetPasswordForm()
    if request.method == "POST":
        email = request.POST.get("email", False)
        if email:
            try:
                new_user = CustomUser.objects.get(email=email)
                token = str(hashlib.sha1(new_user.username + auth_key + new_user.uuid +
                                                 time.strftime('%Y-%m-%d', time.localtime(time.time()))).hexdigest())

                url = u'http://%s/accounts/newpasswd/?uuid=%s&token=%s' % (request.get_host(), new_user.uuid, token)
                mail_title = u'运维自动化初始密码'
                mail_msg = u"""
                Hi,%s:
                    请点击以下链接修改密码,此链接当天有效:
                        %s
                    有任何问题，请随时和运维组联系。
                """ % (new_user.first_name, url)
                #

                send_mail(mail_title, mail_msg, u'运维自动化<devops@funshion.net>', [new_user.email], fail_silently=False)

                return HttpResponseRedirect('/')
            except:
                pass

        return render_to_response('404.html', locals(), context_instance=RequestContext(request))


    return render_to_response('user/reset_password.html', locals(), context_instance=RequestContext(request))