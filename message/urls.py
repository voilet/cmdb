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
    # 资产管理
    url(r'edit_id/(?P<id>\d+)/$', 'assets.value_class.index.server_edit'),
    url(r'^oldnew/', 'message.mail.mail'),
    url(r'^news/', 'message.mail.new_mail'),
    url(r'', 'message.mail.mail'),
)


