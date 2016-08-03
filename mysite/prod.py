#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName: salt_webconfig.py
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2014 14-2-8 上午10:04
#      History:
#=============================================================================


import os

DEBUG = True
website = "http://127.0.0.1"
# salt api config
salt_api_url = "https://127.0.0.1/"
# salt_api_url = "https://salt-api.int.fun.tv/"
salt_api_user = "salt"
salt_api_pass = "8a26fb37f87a1e451daa1085ac597506"

pxe_url_api = "http://192.168.115.180:8888/clone/"

Environment = ['prod', 'beta', 'dev', 'st', 'qa']

# salt auth
auth_content = ['vi', 'vim', 'poweroff', 'shutdown', 'rm', 'init', 'reboot', 'useradd', 'userdel', 'userhelper',
                'usermod', 'usernetctl', 'users', "echo"]

# LOGIN_URL = "http://auth.jumeird.com/api/login/?camefrom=jmops"
app_key = "&app_key=e00acc666d4911e3a268fa163e73f605"
app_name = "&app_name=jmops&key=1"
auth_url = "http://auth.xxx.com/"
auth_key = "e00acc666d4911e3a268fa163e73f605"

# 跳板机使用
springboard = "ea76757b5d91c5c96bf58500a5f7eda0"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        # 'NAME': 'voilet_cmdb_v1',  # Or path to database file if using sqlite3.
        'NAME': 'cmdb_v2',  # Or path to database file if using sqlite3.
         'USER': 'root',
         'PASSWORD': '123456',  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '3306',  # Set to empty string for default. Not used with sqlite3.
        "OPTIONS": {
            "init_command": "SET foreign_key_checks = 0;",
        },
    },

    # 'slave': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'NAME': 'salt',
    #     'USER': 'root',
    #     'PASSWORD': 'wanghui',
    #     'HOST': 'localhost',
    #     'PORT': '3306',
    # }
}

# from pymongo import MongoClient
# client = MongoClient('localhost',27017)
# db = client['config_center']

# salt tornado api
# salt_tornado_api = "http://10.1.2.21:8888/api/"

swan_url = "http://127.0.0.1:8888/swan_api/"
# swan_url = "http://192.168.115.205/swan_api/"

websocket_url = "127.0.0.1:8888/websocket"
# websocket_url = "ops.int.funshion.com/websocket"
ops_mail = "voilet@qq.com"




