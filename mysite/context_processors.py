#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: context_processors.py
#         Desc: 2015-15/3/30:下午6:09
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================
from users.models import CustomUser
from accounts.auth_session import auth_class

def user_session_expiry(request):
    """

    :return:
    """

    user_id = request.session.get('username')
    expirty_data = auth_class(user_id)
    user_id = request.session.get('user_id')
    role_id = request.session.get('role_id')
    user_total_num = CustomUser.objects.all().count()
    user_active_num = CustomUser.objects.filter(is_active=True).count()
    expirty_data["user_id"] = user_id
    expirty_data["role_id"] = role_id
    expirty_data["user_total_num"] = user_total_num
    expirty_data["user_active_num"] = user_active_num
    request.session.set_expiry(28800)

    return expirty_data