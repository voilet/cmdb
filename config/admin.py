#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: admin.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014-05-27
#      History:
#=============================================================================


from django.contrib import admin
from models import *

for cls in [ConfTemplate, OperationLog, Salt_mode_name,]:
    admin.site.register(cls)



