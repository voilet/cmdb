#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: no_auth.py
#         Desc: 2015-15/3/31:上午11:56
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================


def check_auth(request, data):
    if request.user.is_superuser or request.session["fun_auth"].get(data, False):
        return True
    else:
        return False
