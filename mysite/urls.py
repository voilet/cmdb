#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2013-02-20 14:52:11
#      History:
# =============================================================================

from django.conf.urls import patterns, include, url
from mysite.settings import MEDIA_ROOT
from django.contrib import admin
from settings import BASE_DIR

admin.autodiscover()

urlpatterns = patterns('',
                       (r'^upload/(?P<path>.*)$', 'django.views.static.serve', {'document_root': "%s/upload" % BASE_DIR}),

                       url(r'accounts/', include("accounts.urls")),
                       # url(r'^$', 'salt_ui.auto.auto_index_class.auto_index'),
                       url(r'^$', 'salt_ui.views.index.salt_index_new'),
                       url(r'^login/$', 'salt_ui.views.index.auth_login'),
                       url(r'^test/$', 'salt_ui.views.index.test'),
                       # 日志
                       url(r'^logs/salt/', 'salt_ui.views.api_log_class.salt_data_log'),
                       url(r'^logs/host/', "audit.views.audit_list"),

                       # 搜索
                       # url(r'^search/$', 'assets.views.search'),
                       # salt_ui
                       url(r'salt/', include("salt_ui.urls")),
                       # 资产管理
                       url(r'assets/', include("assets.urls")),
                       # url(r'',include(salt_ui.urls)),
                       # 运维自动化
                       url(r'auto/', include("salt_ui.auto.urls")),
                       # 资产api
                       url(r'api/', include("api.urls")),
                       url(r'conf/', include("config.urls")),

                       # 审计模块
                       url(r'^audit/', include("audit.urls")),

                       # admin
                       url(r'^admin/', include(admin.site.urls)),

                       # swan发布接口
                       url(r'swan/', include("swan.urls")),

                       # 故障管理
                       url(r'^incident/', include("malfunction.urls")),

                       # 监控
                       url(r'^monitor/', include("monitor.urls")),

                       # message
                       url(r'^message/', include("message.urls")),

                       # 权限组
                       url(r'^auth/', include("cmdb_auth.urls")),

                       url(r'^ops/doc/$', 'salt_ui.views.index.OpsDoc'),
                       url(r'^api/project/$', 'assets.api.api.type_list'),
                       url(r'^api/project/(?P<id>\d+)/$', 'assets.api.api.type_list_id'),

                       url(r'^ueditor/', include('DjangoUeditor.urls')),


                       # url(r'^summernote/', include('django_summernote.urls')),
                       #
                       )
