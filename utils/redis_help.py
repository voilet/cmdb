#!/usr/bin/env python
#-*- coding: utf-8 -*-
import json
import redis

from mysite.settings import REDIS_HOST, REDIS_PORT, REDIS_DB

conn = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_redis_result(jid):
    ##jid is unix timestamp+some int
    key_list = conn.keys("*"+jid)
    ret = {}
    for one in key_list:
        result = json.loads(conn.get(one))
        ret[result['id']] = result['return']
    return ret

def get_single_result(jid_with_minion):
    ##jid is unix timestamp+some int
    a = conn.get(jid_with_minion)
    result = json.loads(a)
    return result["return"]
#channel name is salt_redis_return

CHANNEL_NAME = "salt_redis_return"

p = conn.pubsub()
# q= p.subscribe(CHANNEL_NAME)
