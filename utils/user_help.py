#!/usr/bin/env python
#-*- coding: utf-8 -*-

from assets.models import ProjectUser
def get_business_by_user(user):
    t_list = ProjectUser.objects.filter(user = user)
    return [one.myform for one in t_list]

def get_user_by_business(business):
    t_list = ProjectUser.objects.filter(myform = business)
    return [one.user for one in t_list]
