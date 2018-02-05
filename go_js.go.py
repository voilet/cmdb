#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: go_js.go
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 2017/9/14 下午10:22
     History:   
"""
import json

s = [
    {"id": 1, "pId": 0, "name": "普通的父节点", "t": "我很普通，随便点我吧", "open": True},
    {"id": 11, "pId": 1, "name": "叶子节点 - 1", "t": "我很普通，随便点我吧", "open": False},
]

print json.dumps(s, indent=4)
