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
from salt_https_api import salt_api_token
from mysite.settings import  salt_api_pass,salt_api_user,salt_api_url


def token_id():
    s = salt_api_token(
        {
        "username":salt_api_user,
        "password":salt_api_pass,
        "eauth":"pam"
        },
        salt_api_url + "login",
        {}
    )
    test = s.run()
    salt_token = [i["token"] for i in test["return"]]
    salt_token = salt_token[0]
    return salt_token

