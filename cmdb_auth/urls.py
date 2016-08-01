#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 
#      History:
# =============================================================================

from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^cmdb/add/$', "cmdb_auth.views.cmdb_auth"),
                       url(r'^cmdb/status/(?P<uuid>[^/]+)/$', "cmdb_auth.views.edit_status"),
                       url(r'^cmdb/group_auth/(?P<uuid>[^/]+)/$', "cmdb_auth.views.add_auth"),
                       url(r'^cmdb/group_user/(?P<uuid>[^/]+)/$', "cmdb_auth.views.add_group_user"),
                       url(r'^cmdb/group_auth_delete/(?P<uuid>[^/]+)/$', "cmdb_auth.views.delete_auth"),
                       url(r'^cmdb/group_auth_edit/(?P<uuid>[^/]+)/$', "cmdb_auth.views.edit_auth"),

                       # 发布权限
                       url(r'^swan_auth/push_auth/$', "cmdb_auth.views.auth_swan"),
                       url(r'^swan_auth/group_user/(?P<uuid>[^/]+)/$', "cmdb_auth.views.auth_swan_user"),

                       # 服务器授权
                       url(r'host/user_list/$', "cmdb_auth.views.user_select"),
                       url(r'host/business/$', "cmdb_auth.views.ztree_business"),
                       url(r'host/add_host/(?P<uuid>[^/]+)/$', "cmdb_auth.views.user_auth_server", name="add_auth"),
                       url(r'node/(?P<uuid>[^/]+)/$', "cmdb_auth.views.user_count", name="node_count"),

                       url(r'^cmdb/$', "cmdb_auth.views.auth_index"),
                       )
