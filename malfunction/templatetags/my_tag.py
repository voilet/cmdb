#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: Incldent.py
#         Desc: 2015-15/6/5:下午4:45
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django import template
from malfunction.models import Incident

register = template.Library()


@register.filter(name='myIncident')
def myIncident(username):
    data = Incident.objects.filter(projectuser=username, status__lte=1).count()

    return data


@register.filter(name='myClassical')
def myClassical(username):
    data = Incident.objects.filter(classical=True).count()
    return data


@register.filter(name='NoDone')
def NoDone(username):
    data = Incident.objects.filter(status__lte=1).count()
    return data


@register.filter(name='Done')
def Done(username):
    data = Incident.objects.filter(status=2).count()
    return data

