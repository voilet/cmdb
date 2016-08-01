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
from cmdb_auth.models import AuthNode
from users.models import CustomUser

register = template.Library()

@register.filter(name='node_count')
def node_count(user):
    user = CustomUser.objects.get(username=user)
    user_count = AuthNode.objects.filter(user_name=user).count()

    return user_count

