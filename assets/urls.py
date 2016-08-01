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
from assets import views, service_views, salt_cdn_cmdb

urlpatterns = patterns('',
                       # 资产管理
                       url(r'^server/select_business/$', 'assets.value_class.index.select_business',
                           name="select_business"),
                       url(r'^server/update_cabinet/$', 'assets.value_class.index.update_cabinet',
                           name="update_cabinet"),
                       url(r'^server/update_system/$', 'assets.value_class.index.update_system',
                           name="update_system"),
                       url(r'^server/host_without_business/', 'assets.value_class.index.host_without_business'),
                       url(r'^server/auth_without_business/$',
                           'assets.value_class.index.auth_host_without_business'),
                       url(r'^server/restart/(?P<uuid>[^/]+)/', 'assets.value_class.index.restart_node', name="install_system"),
                       url(r'^host_detail/$', "assets.views.host_detail", name="host_detail"),
                       url(r'^host_list/$', "assets.views.host_list"),
                       url(r'^host_add/$', "assets.views.host_add"),
                       url(r'^host_edit/$', "assets.views.host_edit", name="host_edit"),
                       url(r'^host_edit_batch/$', "assets.views.host_edit_batch"),
                       url(r'^host_update/$', "assets.views.host_update"),
                       url(r'^host_del/$', "assets.views.host_del", name='host_del'),
                       url(r'^host_del_batch/$', "assets.views.host_del_batch"),
                       url(r'^host_add_batch/$', "assets.views.host_add_batch"),
                       url(r'^change_info_ajax/$', "assets.views.host_search"),
                       url(r'^host_search/$', "assets.views.host_search"),
                       url(r'^idc_add/$', "assets.views.idc_add"),
                       url(r'^idc_list/$', "assets.views.idc_list"),
                       url(r'^idc_edit/$', "assets.views.idc_edit"),
                       url(r'^idc_del/$', "assets.views.idc_del"),
                       url(r'^zabbix/$', "assets.views.zabbix_info"),
                       url(r'^zabbix_host/$', "assets.views.zabbix_host"),
                       url(r'^ip_list/$', "assets.views.ip_list"),
                       url(r'^ip_list_ajax/$', "assets.views.ip_list_ajax"),
                       url(r'^ip_list_info/$', "assets.views.ip_list_info"),
                       url(r'^test/$', "assets.salt_cdn_cmdb.test"),

                       # 机房操作
                       url(r'server/room/add/', 'assets.value_class.Engine_room.add_room'),
                       url(r'server/room/list/', 'assets.value_class.Engine_room.room_list'),
                       url(r'server/room/edit/(?P<id>\d+)/$', 'assets.value_class.Engine_room.room_edit'),
                       url(r'server/room/delete/(?P<id>\d+)/$', 'assets.value_class.Engine_room.room_delete'),

                       # 服务操作
                       url(r'service_add/$', "assets.service_views.service_add"),
                       url(r'service_edit/$', "assets.service_views.service_edit"),
                       url(r'service_list/$', "assets.service_views.service_list"),
                       url(r'service_del/$', "assets.service_views.service_del"),

                       # 项目管理
                       url(r'^server/user_auth/$', 'assets.value_class.business.server_type_auth',
                           name="user_idc_auth_server"),
                       url(r'^server/type/item_ajax/$', 'assets.value_class.business.business_item_ajax',
                           name="business_item_ajax"),
                       url(r'^server/type/(?P<uuid>[^/]+)/host_list/$',
                           'assets.value_class.business.business_host_list', name="business_host_list"),
                       url(r'^server/type/add/', 'assets.value_class.business.server_type_add'),
                       url(r'^server/type/list/', 'assets.value_class.business.auth_server_type_list', name='project_list'),

                       url(r'^server/type/edit/(?P<uuid>[^/]+)/$',
                           'assets.value_class.business.auth_server_type_edit', name="project_edit_ajax"),
                       url(r'^server/type/del/(?P<uuid>[^/]+)/$',
                           'assets.value_class.business.auth_server_type_del'),

                       url(r'^server/type/doc/(?P<uuid>[^/]+)/$', 'assets.value_class.business.project_doc',
                           name="project_doc"),
                       url(r'^server/type/edit_doc/(?P<uuid>[^/]+)/$',
                           'assets.value_class.business.project_doc_edit', name="project_doc_edit"),

                       url(r'^server/server_type/$', 'assets.value_class.business.server_type_item'),

                       # 项目用户
                       url(r'^server/type/edit/(?P<uuid>[^/]+)/user/$',
                           'assets.value_class.business.auth_server_type_user_select', name="business_user_edit"),
                       url(r'^server/type/edit/(?P<uuid>[^/]+)/user/add/$',
                           'assets.value_class.business.auth_server_type_user_add', name="business_user_add"),
                       url(r'^server/type/edit/(?P<id>\d+)/user/edit/$',
                           'assets.value_class.business.auth_server_type_user_edit', name="business_useredit"),
                       url(r'^server/type/edit/(?P<id>\d+)/user/delete/$',
                           'assets.value_class.business.auth_server_type_user_delete'),

                       # 操作日志
                       url(r'^server/batch/', 'assets.value_class.index.Index_add_batch'),

                       url(r'^server/bat/.*$', 'assets.value_class.index.batadd'),
                       url(r'^server/order_by/.*$', 'assets.value_class.index.server_order_by'),
                       url(r'^search/.*$', 'assets.value_class.index.Node_search', name="search"),
                       url(r'^cabinet/.*$', 'assets.value_class.index.search_cabinet', name="cabinet"),
                       url(r'^default/$', 'assets.value_class.index.select_default', name="default"),
                       url(r'^select', 'assets.value_class.index.Node_select'),
                       url(r'^filter/', 'assets.value_class.index.node_filter'),
                       # url(r'test_update/.*$', 'assets.value_class.index.node_update'),
                       # 添加业务线
                       url(r'^product/add/$', 'assets.value_class.product_line.product_add', name="product_add"),
                       url(r'^product/edit/(?P<uuid>[^/]+)/$', 'assets.value_class.product_line.product_edit',
                           name="product_edit"),
                       url(r'^product/list/$', 'assets.value_class.product_line.product_list', name="product_list"),

                       url(r'^server/install/$', 'assets.value_class.index.txt_update'),

                       # ztree
                       url(r'^ztree/project/$', 'assets.ztree.api.ztree_project'),
                       url(r'^ztree/business/$', 'assets.ztree.api.ztree_business'),
                       url(r'^ztree/cdn/$', 'assets.ztree.api.CdnCache'),
                       url(r'^ztree/idc/$', 'assets.ztree.api.CdnIdc'),

                       #   服务查询
                       url(r'^ztree/service/(?P<uuid>\w+)/$', 'assets.ztree.service.ServiceStatus',
                           name="service_status"),
                       url(r'^ztree/service/$', 'assets.ztree.service.ztree_service'),
                       url(r'^ztree/$', 'assets.ztree.api.ZtreeIndex'),
                       url(r'^markdown/select/(?P<uuid>[^/]+)/', "assets.views.MarkDown_content", name="MarkDown_content"),
                       url(r'^markdown/edit/(?P<uuid>[^/]+)/$', "assets.views.MarkDown_edit", name="MarkDown_edit"),
                       url(r'^markdown/', "assets.views.MarkDown_edit", name="MarkDown_edit"),
                       url(r'^server/$', 'assets.views.host_list'),
                       # url(r'$/', "assets.views.host_list"),

                       )
