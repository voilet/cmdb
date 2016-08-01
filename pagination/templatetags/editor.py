# !/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: editor.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-06-12
#      History: 
#=============================================================================
import datetime
from django import template

register = template.Library()

def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

register.simple_tag(current_time)

def editor(context):
    return {}
register.inclusion_tag('saltstack/editor.html', takes_context=True)(editor)
