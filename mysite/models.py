#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: models.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014 14-1-24 下午5:35
#      History:
#=============================================================================

class DBRouter(object):

    def db_for_read(self, model, **hints):
        return 'slave'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_syncdb(self, db, model):
        return None