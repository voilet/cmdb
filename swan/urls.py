#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: urls.py
#         Desc: 2015-15/1/5:下午1:20
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.conf.urls import patterns, url




urlpatterns = patterns('',
    # 项目配置自动化发布
    url(r'push/$', "swan.views.swan_push"),
    url(r'release/$', "swan.views.swan_release"),
    url(r'log/(?P<uuid>[^/]+)/$$', "swan.views.SwanSelectLog", name="SwanSelectLog"),
    url(r'swan_select/$', "swan.views.swan_select"),
    url(r'^swan_select_myfrom/$', "swan.views.swan_select_myfrom"),
    url(r'^swan_select_botton/$', "swan.views.swan_select_button"),
    url(r'swan_select_tgt/$', "swan.views.swan_select_tgt"),
    url(r'^websocket/$', "swan.views.swan_websocket"),
    url(r'^apply/(?P<uuid>[^/]+)/$', "swan.views.swan_apply"),
    url(r'^apply/p/$', "swan.views.apply_project"),
    url(r'^apply/exec/$', "swan.views.apply_auto"),
    url(r'$', "swan.views.swan_index"),
)


