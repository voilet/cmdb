#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: urls.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-02-27
#      History: 
# =============================================================================

from django.conf.urls import patterns, url
from config.operation import *

urlpatterns = patterns('',
                       url(r'^$', "config.add_config_class.salt_conf_index"),
                       url(r'^add/$', "config.add_config_class.add_conf_class"),
                       url(r'^list/$', "config.add_config_class.list_conf_class"),
                       url(r'^list/(?P<pk>\d+)/$', "config.add_config_class.item_conf_class"),
                       url(r'^edit/(?P<pk>\d+)/$', "config.add_config_class.edit_conf_class"),

                       url(r'^add_log/$', new_log),
                       url(r'^log_list/$', log_list),
                       url(r'^log_mail_restart/(?P<id>\d+)/', mail_restart, name="mail_restart"),

                       # url(r'sls/add/$', sls_add),
                       # url(r'sls/list/$', sls_list),
                       # url(r'sls/edit/(?P<id>\d+)/$', sls_edit),
                       # url(r'sls/del/(?P<id>\d+)/$', sls_del),

                       # 项目配置自动化发布
                       url(r'project/code/add/', "config.project_conf.Code_add", name='add_code'),
                       # url(r'project/add/(?P<uuid>[^/]+)/default/', "config.project_conf.project_add",
                       #     name="swan_default"),
                       # url(r'project/add/(?P<uuid>[^/]+)/config/', "config.project_conf.project_add",
                       #     name="swan_config"),
                       url(r'project/add/(?P<uuid>[^/]+)/git/', "config.project_conf.project_git", name="swan_git"),
                       url(r'project/add/(?P<uuid>[^/]+)/java/', "config.project_conf.projectJava", name="swan_java"),
                       url(r'project/add/(?P<uuid>[^/]+)/shell/', "config.project_conf.project_shell", name="swan_shell"),
                       url(r'project/add/(?P<uuid>[^/]+)/$', "config.project_conf.project_add"),
                       url(r'project/edit/(?P<uuid>[^/]+)/(?P<id>[^/]+)/$', "config.project_conf.project_edit"),

                       )
