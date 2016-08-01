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


from assets.models import Host, IDC, Server_System, Cores, System_os, system_arch

server_data = open('/Users/voilet/opsautomation/jumei_optools/scripts/server_list.txt', 'r')
data = server_data.readlines()
server_data.close()

for i in data:
    s = i.split()
    # print i
    host_data = Host(node_name=s[0], idc_id=1, eth1=s[0], brand="DELL", internal_ip=s[1], cabinet=s[2], editor=s[3], auto_install=1, sort="default")
    host_data.save()


