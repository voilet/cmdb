#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: forms.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/27 下午3:46
     History:   
"""

from models import MonitorHttp, MonitorHttpLog
from django import forms

BOOL_CHOICES = ((True, 'GET'), (False, 'POST'))
BOOL_RESULT = ((True, 'http状态'), (False, '返回值'))
BOOL_STATUS = ((True, '是'), (False, '否'))


class MonitorHttpForm(forms.ModelForm):
    monitor_type = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_CHOICES, required=True, initial=True,
                                     label=u"请求类型")
    result_code = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_RESULT, required=True, initial=True,
                                    help_text=u'中选择retCode则需要接口返回json数据',
                                    label=u"监控项")

    mail_status = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_STATUS, required=True, initial=True,
                                    label=u"邮件报警")
    status = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_STATUS, required=True, initial=True,
                               label=u"是否启用")
    weixin_status = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_STATUS, required=True, initial=True,
                                      help_text=u'微信报警需先加入团队号',
                                      label=u"微信报警")

    class Meta:
        model = MonitorHttp
        fields = [
            "title",
            "url",
            "monitor_type",
            "monitor_ip",
            "result_code",
            "mail_status",
            "mail",
            "weixin_status",
            "weixin",
            "payload",
            "status",
        ]


class MonitorLogForm(forms.ModelForm):
    class Meta:
        model = MonitorHttpLog
        fields = [
            "monitorId",
            "monitor_title",
            "content",
            "code",
            "job_id"
        ]
