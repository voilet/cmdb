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

# Uncomment the next two lines to enable the admin:
import salt_ui.views.index
import salt_ui.views.api_log_class
from salt_ui.views.cmd_node import salt_cmd_node
from salt_ui.views.update_node import salt_update_node
from salt_ui.auto.auto_index_class import auto_index, services_install_all
from cmd import cmd_run, handle_redis, highstate_redis, button_cmd_run
from salt_highstate import salt_highstate

urlpatterns = patterns('',
                       # 自动化
                       # url(r'^reject_apply/$', salt_ui.auto.auto_index_class.reject_apply),
                       url(r'install_node/', salt_ui.auto.auto_index_class.services_install_setup_node),
                       # url(r'install/', salt_ui.auto.auto_index_class.services_install_all),
                       url(r'init/', salt_ui.auto.auto_index_class.services_install_init),
                       url(r'sls/', salt_ui.auto.auto_index_class.sls_install_init),
                       url(r'setup/list/(?P<id>\d+)/', salt_ui.auto.auto_index_class.install_id_setup),
                       url(r'setup/(?P<id>\d+)/', salt_ui.auto.auto_index_class.sls_install_id),
                       url(r'setup/', salt_ui.auto.auto_index_class.sls_install_setup),
                       # url(r'apply/', salt_ui.auto.auto_index_class.apply_install),
                       # url(r'approve/', salt_ui.auto.auto_index_class.approve_install),
                       url(r'setup_log/(?P<pk>\d+)/', salt_ui.auto.auto_index_class.log_list),

                       # 自动化运维首页
                       url(r'^$', salt_ui.auto.auto_index_class.auto_index),
                       url(r'^salt_cmd/$', "salt_ui.auto.cmd.cmd_run", name="cmd_run"),
                       url(r'^button_cmd_run/$', button_cmd_run, name="button_cmd_run"),
                       url(r'^highstate/$', salt_highstate, name="highstate"),
                       url(r'^redis/$', handle_redis, name="handle_redis"),
                       url(r'^highstate/redis/$', highstate_redis, name="highstate_redis"),

                       )
