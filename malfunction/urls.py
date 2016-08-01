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
from assets import views, service_views, salt_cdn_cmdb

urlpatterns = patterns('',

    url(r'^add/$', "malfunction.views.FaultAdd"),
    url(r'^my/$', "malfunction.views.FaultMy"),
    url(r'^nodone/$', "malfunction.views.FaultNoDone", name="FaultNoDone"),
    url(r'^done/$', "malfunction.views.FaultDone"),
    url(r'^source/$', "malfunction.views.FaultSource"),
    url(r'^classical/$', "malfunction.views.FaultClassical"),
    url(r'^edit/(?P<uuid>[^/]+)/$', "malfunction.views.FaultEdit"),
    url(r'^(?P<uuid>[^/]+)/$', "malfunction.views.FaultDetail"),
    url(r'$', "malfunction.views.FaultIndex"),
)


