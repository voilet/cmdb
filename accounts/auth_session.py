#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName: auth_session.py
#         Desc: 2015-15/3/30:下午1:45
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from cmdb_auth.models import user_auth_cmdb, auth_group

def auth_class(user):
    """
    修改session权限
    刷新页面权限即生效
    :return:
    """
    auth_group_data = {}
    auth_list = [
        "select_host",
        "edit_host",
        "update_host",
        "add_host",
        "bat_add_host",
        "delete_host",
        "project_name",
        "add_user",
        "edit_user",
        "edit_pass",
        "delete_user",
        "add_department",
        "add_idc",
        "edit_idc",
        "del_idc",
        "setup_system",
        "upload_system",
        "salt_keys",
        "project_auth",
        "auth_log",
        "add_project",
        "edit_project",
        "del_project",
        "select_idc",
        "auth_project",
        "auth_highstate",
        "cmdb_log",
        "server_audit",
    ]

    user_name = user
    if user_name:
        group_auth = user_name.auth_group_set.all().filter(enable=True)
        # 权限
        for auth_uuid in group_auth:
            uuid = str(auth_uuid.uuid)
            data = auth_group.objects.get(uuid=uuid)
            try:
                auth_info = user_auth_cmdb.objects.get(group_name=data)

                for i in auth_list:
                    try:
                        s = getattr(auth_info, i)
                        if s:
                            print auth_group_data.get(i)
                            auth_group_data[i] = s

                    except AttributeError:
                        pass
            except user_auth_cmdb.DoesNotExist:
                pass
        return auth_group_data
    else:
        return auth_group_data