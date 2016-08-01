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


urlpatterns = patterns('',
    #资产管理
    url(r'^project/$', 'assets.api.api.type_list'),
    url(r'^project/(?P<id>\d+)/$', 'assets.api.api.type_list_id'),
    url(r'^user/.*$', 'assets.api.api.user_select'),

    #装机操作
    url(r'^sn/.*$', 'assets.api.api.Sn_number'),
    url(r'^cmdb/.*$', 'assets.api.api.CmdbUpdate'),

    #nagios监控接口

    url(r'^audit/list/.*$', 'audit.views.audit_list'),

    url(r'^audit/$', 'audit.views.audit_save'),
    # url(r'^create', 'assets.api.api.saltstack_create_config'),

    #安装完成上报接口
    url(r'^system_install/$', 'assets.value_class.index.install_ok'),
    url(r'^alert/$', 'malfunction.views.FaultApi'),

)


