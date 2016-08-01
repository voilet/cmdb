#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: zabbix
#         Desc: 2015-15/5/27:下午4:24
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django import template
from assets.zabbix import zabbix_get_item, zabbix_get_trigger, zabbix_get_item_count, zabbix_get_trigger_count

register = template.Library()

@register.filter(name='zabbix_count')
def zabbix_count(ip):
    count = zabbix_get_item_count(ip)
    if count:
        return count
    return False


@register.filter(name='zabbix_caveat')
def zabbix_caveat(ip):
    caveat = zabbix_get_trigger_count(ip)

    if caveat:
        return caveat

    return False