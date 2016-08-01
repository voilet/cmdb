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
                       url(r'^http/add/$', "monitor.views.HttpMonitor", name="HttpMonitor"),
                       url(r'^http/edit/(?P<uuid>[^/]+)/', "monitor.views.HttpMonitorEdit", name="HttpMonitorEdit"),
                       url(r'^http/status/(?P<uuid>[^/]+)/$', "monitor.views.HttpMonitorstatus", name="HttpMonitorstatus"),
                       url(r'^http/del/(?P<uuid>[^/]+)/$', "monitor.views.HttpMonitorDel", name="HttpMonitorDel"),
                       url(r'^http/detail/(?P<uuid>[^/]+)/', "monitor.views.HttpMonitorPage", name="HttpMonitorPage"),
                       url(r'^http/list/$', "monitor.views.HttpMonitorlist", name="httpmonitorlist"),
                       )
