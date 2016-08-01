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

from django.conf.urls import patterns, url

import salt_ui.views.index
import salt_ui.views.server_type_node
import salt_ui.views.api_log_class
from salt_ui.views.cmd_node import salt_cmd_node
from salt_ui.views.update_node import salt_update_node
import salt_ui.views.key

urlpatterns = patterns('',
    #salt_key
    url(r'^key_list/$', "salt_ui.views.key.salt_key_list"),
    url(r'^delete_key/$', "salt_ui.views.key.salt_delete_key"),
    url(r'^accept_key/$', "salt_ui.views.key.salt_key_accept"),
    #salt_ui

    url(r'cmd/$', "salt_ui.views.index.salt_cmd"),
    url(r'garins/$', "salt_ui.views.index.salt_garins"),
    url(r'node_shell/$', "salt_ui.views.index.salt_check_setup"),
    url(r'node_server/$', "salt_ui.views.index.salt_state_sls"),
    url(r'update_node/.*$', "salt_ui.views.update_node.salt_update_node"),
    url(r'logs/$', "salt_ui.views.api_log_class.salt_data_log"),
    url(r'cmd_node/$', "salt_ui.views.cmd_node.salt_cmd_node"),


    url(r'key/', "salt_ui.views.key.salt_key"),
    url(r'^commands/', "salt_ui.views.index.salt_cmd_commands"),
    url(r'^status/$', "salt_ui.views.index.status"),
    url(r'^node_list/', "salt_ui.views.index.salt_node_list"),
    url(r'help/', "salt_ui.views.index.salt_help"),
    url(r'jid/$', "salt_ui.views.jid_api.salt_jid_select"),
    url(r'^jobs/$', "salt_ui.auto.salt_highstate.JobsJid"),

    #安装系统
    url(r'^install/', "salt_ui.auto.auto_index_class.services_install_all"),
    url(r'', "salt_ui.views.index.salt_index"),


)


