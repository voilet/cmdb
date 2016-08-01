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


from django.contrib import admin
from salt_ui.models import *

class SetupLogAdmin(admin.ModelAdmin):
    list_display = ('user','business','status', 'content','approve_user','reject_reason','approve_time','date_created')


for cls in [salt_conf,salt_api_log]:
    admin.site.register(cls)

admin.site.register(SetupLog, SetupLogAdmin)
