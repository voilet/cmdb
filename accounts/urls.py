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

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
import accounts.views
import accounts.account
import accounts.user_mode.user_edit_class


urlpatterns = patterns('',
    #user
    # url(r'(?P<id>\d+)/$',salt_ui.views.index.salt_status),
    url(r'^login/$', "accounts.account.user_login"),
    url(r'^edit_passwd/$', "accounts.account.change_password"),
    url(r'^newpasswd/$', "accounts.account.new_password"),
    url(r'^resetpass/$', "accounts.account.Resetpassword"),
    url(r'adduser/$', "accounts.views.register"),
    url(r'user_list/$', "accounts.views.user_select", name='user_list'),
    url(r'^status/(?P<id>\d+)/$', "accounts.views.user_status"),
    url(r'^delete/(?P<id>\d+)/$', "accounts.views.user_delete"),
    url(r'^old/$', "accounts.views.user_old"),
    url(r'^user_static/$', "accounts.views.user_list_status"),
    url(r'add_department/$', "accounts.views.department_view"),
    url(r'department/edit/(?P<id>\d+)/$', "accounts.views.department_edit"),
    url(r'list_department/$', "accounts.views.department_list"),
    url(r'user_edit/(?P<id>\d+)/$', "accounts.user_mode.user_edit_class.user_edit"),
    url(r'user/', "accounts.user_mode.user_edit_class.user_update"),
    # url(r'user/', "accounts.account.change_password"),
    url(r'user/(?P<id>\d+)/$', "accounts.user_mode.user_edit_class.user_id"),
    url(r'^loginout/$', "accounts.views.logout_view"),
    url(r'^password/$', 'django.contrib.auth.views.password_change', {'template_name': 'user/user_editpassword.html', 'post_change_redirect': '/'}),

    #添加服务器权限
    url(r'server/auth/add/(?P<uuid>[^/]+)/$', "accounts.user_mode.server_auth.user_auth_server", name="add_auth"),
    url(r'^server/auth/delete/$', "accounts.user_mode.server_auth.user_auth_delete", name="delete_auth"),
    url(r'server/auth/ip/$', "accounts.user_mode.server_auth.server_auth_ip"),
    url(r'auth/$', "accounts.user_mode.server_auth.server_auth_user"),
    url(r'test/$', "accounts.views.user_auth_node"),
    url(r'menu/$', "accounts.views.menu_class"),
)


