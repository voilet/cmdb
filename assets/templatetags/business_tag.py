#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: business_tag.py
#         Desc: 2015-15/4/22:下午11:18
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

import ast

from django import template
from assets.models import Host, Project

register = template.Library()

@register.filter(name='business_list')
def business_list(host):
    cmdb_data = Host.objects.get(pk=host)
    data = cmdb_data.business.all()

    business_all = []
    for i in data:
        business_all.append(i.service_name)

    return business_all

@register.filter(name='business_service')
def business_service(name):
    s = []
    bus_data = Project.objects.get(service_name=name)
    server_list = Host.objects.filter(business=bus_data).order_by("id")

    for i in server_list:
        t = i.service.all()
        for b in t:
            if b not in s:
                s.append(b)

    return s


@register.filter(name='group_str2')
def groups_str2(group_list):
    if len(group_list) < 3:
        return ' '.join([group.name for group in group_list])
    else:
        return '%s ...' % ' '.join([group.name for group in group_list[0:2]])


@register.filter(name='get_vm_info')
def get_vm_info(host_id):
    host = Host.objects.get(uuid=host_id)
    vm = Host.objects.filter(vm=host)
    if vm:
        return vm
    else:
        return False

@register.filter(name='str_to_list')
def str_to_list(info):
    return ast.literal_eval(info)