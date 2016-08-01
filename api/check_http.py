#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: check_http.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/28 下午8:27
     History:   
"""
import sys
import os

reload(sys)
sys.setdefaultencoding('utf8')
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

from monitor.models import MonitorHttp

uurl_list = {
    "adm": {
        "url": [
            'http://ad.funshion.com/control/adredirect.html',
            'http://ad.funshion.com/control/ad_define.fai',
            'http://ad.funshion.com/pause/?c=shy,,',
            'http://adm.funshion.com/ad/2010-12/19CA07D0_07AE_9F44_52D2_481FAB1722F4.swf',
        ],
        "project_name": u"广告",
        "ip": [
            "220.181.167.62",
            "220.181.167.46",
            "220.181.167.52",
            # "220.181.167.53",
            "220.181.167.54",
            "220.181.167.55",
            "220.181.167.56"
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|tianning",
    },
    "weiju": {
        "url": [
            'http://mc.funshion.com/interface/mc?mc=1',
            'http://mc.funshion.com/interface/cc?cc=1',
            'http://pub.funshion.com/interface/deliver?ap=c_b_1',
            'http://pub.funshion.com/interface/monitor?uid=&mac=&fck=9B9D1F39F94CD9D7E84FDFB413677674&ap=c_b_1&matid=530&ad=1795&mid=&reqId=b4251050-9772-11e2-a3ba-79461cd3ded8&t=',
            'http://pub.funshion.com/interface/materials?ap=c_b_1',
            'http://conf.funshion.com/interface/config?client=pc&file=pc-aconfig&ver=2.8.5.24&fmt=xml',
            'http://conf.funshion.com/interface/config?client=ipad&ver=2.8.5.24&fmt=json&file=ipad-aconfig',
            'http://vs.funshion.com/vvs/getMediaUrl/v2',
            'http://vs.funshion.com/pvs/getSchedule/v2',
        ],
        "project_name": u"微距",
        "ip": [
            "220.181.167.89",
            "220.181.167.90",
            "220.181.167.85",
            "220.181.167.86",
            "220.181.167.87",
            "220.181.167.88",
            "220.181.167.91",
            "220.181.167.92",
            "220.181.167.93"
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|tianning",
    },
    "fld": {
        "url": [
            'http://fld.funshion.com/interface/app?aid=999',
            'http://fld.funshion.com/interface/platform?pid=3&ver=0.0.0.72',
            'http://fld.funshion.com/interface/airport?cid=1009001&ver=0.0.0.4',
            'http://fld.funshion.com/instant/instant?bid=18',
        ],
        "project_name": u"TK后台",
        "ip": [
            "220.181.167.62",
            "220.181.167.46",
            "220.181.167.52",
            # "220.181.167.53",
            "220.181.167.54",
            "220.181.167.55",
            "220.181.167.56"
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|tianning",
    },
    "pay": {
        "url": [
            'http://pay.funshion.com/',
            'http://pay.funshion.com/api/index.php?opt=get_user_money&user_name=qwer1233&sign=0fde413c05c1320459f49ba340e5e780',
        ],
        "project_name": u"充值",
        "ip": [
            '114.66.198.20',
            '114.66.198.21',
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg",
    },
    "fs": {
        "url": [
            'http://static.funshion.com/css/default.css?20101130',
            'http://www.fun.tv/live/',
            'http://fs.fun.tv/live/',
            'http://www.fun.tv/',
            'http://fs.fun.tv/',
            'http://fs.funshion.com/publish/first?ver=5',
            'http://fs.fun.tv/publish/first?ver=5',
            'http://api.funshion.com/embed_zone',
            'http://img.funshion.com/attachment/images/2008/08-04/5372255_1217833540_699_m.jpg',
            'http://push.funshion.com/api/reset_badge.php?devicetoken=(null)',
            'http://api.fun.tv/embed_zone',
            'http://api.fun.tv/ajax/get_media_data/publish/115616',
            'http://api1.fun.tv/ajax/channel_panel/500780?isajax=1&dtime=1422864772604',
            'http://q1.fun.tv/flash.php?mediaid=0&rand=0.9831538121215999',
            'http://app.fun.tv/app/aphone/list.html?type=movie&order=pl&page=2&cate=#E5#96#9C#E5#89#A7&region=&rdate=&karma=&pagesize=20&clarity=&h',
            'http://www.btstream.org/fsp/2012-02-02/23623226_1328165528_733.fsp',
            'http://imgb.funshion.com/fsp/2012-02-02/23623226_1328165528_733.fsp',
            'http://q.funshion.com/api/torrents/94114/cf01b79e2d80166/4862ef8ce74118f933c0b1a8bb285a0d6a78370a',
            'http://q.funshion.com/v5/getfsp/94209?h=1',
            'http://imgq.funshion.com/api/torrents/94114/cf01b79e2d80166/4862ef8ce74118f933c0b1a8bb285a0d6a78370a',
            'http://imgq.fun.tv/api/torrents/94114/cf01b79e2d80166/4862ef8ce74118f933c0b1a8bb285a0d6a78370a',
        ],
        "project_name": u"网站",
        "ip": [
            '123.125.20.38',
            '123.125.20.39',
            '114.66.198.50',
            '114.66.198.51',
            '114.66.198.52',
            '114.66.198.53',
            '114.66.198.54',
            '114.66.198.55',
            '220.181.167.5',
            '220.181.167.6',
            '220.181.167.7',
            '220.181.167.8',
            '220.181.167.9',
            '220.181.167.13',
            '220.181.167.11',
            '220.181.167.20',
            '220.181.167.21',
            '220.181.167.25',
            '220.181.167.26',
            '220.181.167.27',
            # '222.35.250.34',
            # '222.35.250.35',
            # '222.35.250.47',
            # '222.35.250.48',
            # '222.35.250.49',
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|tianning",
    },
    "poseidon": {
        "url": [
            'http://po.funshion.com/v5/config/homepage?cl=aphone',
            'http://pm.funshion.com/v5/media/topics?channel=cartoon',
            'http://pv.funshion.com/v5/video/topics/?channel=sport',
            'http://ps.funshion.com/v5/search/media?q=%E5%89%91&cl=iphone',
            'http://ps.funshion.com/v7/search/media?q=星球大战&pg=1&sz=100&uc=3',
            'http://pu.funshion.com/v5/user/platform/?cl=ipad&ve=1.1.1.1&fudid=123456&uc=1',
        ],
        "project_name": u"波塞冬",
        "ip": [
            '220.181.167.5',
            '220.181.167.6',
            '220.181.167.7',
            '220.181.167.8',
            '220.181.167.9',
            '220.181.167.13',
            '220.181.167.11',
            '220.181.167.20',
            '220.181.167.21',
            '220.181.167.25',
            '220.181.167.26',
            '220.181.167.27',
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|zhubb",
    },
    "partner": {
        "url": [
            'http://partner.funshion.com/partner/install_statistic.php?s=001D7D3F57DF&id=&c=39e1b8fa03c0c1dcb41b5cc70dde2744&t=first&u=&v=2.3.0.16&auto=0&other=10000000100&mh=1&guid=A835EE1C906144559D6D0EFDF0976C33',
        ],
        "project_name": u"partner",
        "ip": [
            '114.66.198.50',
            '220.181.167.9',
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg",
    },
    "oxeye": {
        "url": [
            'http://stat.funshion.net/monitory/jiankongbao?test=1',
        ],
        "project_name": u"partner",
        "ip": [
            '120.131.127.50',
            '120.131.127.51',
            '120.131.127.52',
            '120.131.127.53',
            '120.131.127.54',
            '120.131.127.55',
            # '120.131.127.56',
            '114.66.198.43',
            '114.66.198.44',
            '114.66.198.57',
            '114.66.198.58',
            '114.66.198.59',
        ],
        "weixin": True,
        "monitor": "songxs|guojy|zhangzhang|wangxg|tianning",
    },
    "bbs": {
        "url": [
            'http://bbs.fun.tv',
        ],
        "project_name": u"电视bbs",
        "ip": [
            "192.168.123.11",
        ],
        "weixin": True,
        "monitor": "songxs|zhangzhang|guojy|zengyc|liyajie|tianning",
    },
    "tv_hive": {
        "url": [
            'http://hive.fun.tv/server_status',
        ],
        "project_name": u"蜂巢",
        "ip": [
            "192.168.115.186",
            "192.168.115.187",
        ],
        "weixin": True,
        "monitor": "songxs|zhangzhang|guojy|zhengxf",
    },
}

for k, v in uurl_list.items():
    """
    title = models.CharField(max_length=120, verbose_name=u"监控名称")
    url = models.TextField(verbose_name=u'监控url', help_text=u'同一组服务器多个url监控换行即可')
    monitor_type = models.BooleanField(default=True, verbose_name=u'请求方式')
    monitor_ip = models.TextField(verbose_name=u'ip列表')
    mail_status = models.BooleanField(verbose_name=u"是否邮件报警", default=True)
    mail = models.TextField(verbose_name=u'邮件联系人', help_text=u'多个邮件联系人换行即可')
    weixin_status = models.BooleanField(verbose_name=u'是否微信报警', default=True)
    weixin = models.TextField(verbose_name=u'微信联系人', help_text=u'多个联系人换行即可')
    payload = models.TextField(verbose_name=u'post数据', null=True, blank=True, help_text=u'POST提交数据,需json格式')
    status = models.BooleanField(verbose_name=u'状态', default=True)
    result_code = models.BooleanField(verbose_name=u'header/code', default=True,
                                      help_text=u'默认监控http status,如果选择为返回值,则监控返回数据retCode是否为200')
    """
    # print k, v["url"]
    check_url = ""
    check_ip = ""
    for i in v["url"]:
        check_url += "%s\n" % i
    for i in v["ip"]:
        check_ip += "%s\n" % i
    # print check_url
    # print check_ip
    check_weixin = str(v["monitor"]).replace("|", "\n")
    s = MonitorHttp(title=k, url=check_url, monitor_type=True, monitor_ip=check_ip, mail_status=True, mail="OP@fun.tv",
                    weixin_status=True, weixin=check_weixin, status=True)
    s.save()
