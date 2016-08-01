#coding:utf-8
from django import VERSION
if VERSION[0:2]>(1,3):
    from django.conf.urls import patterns, url
else:
    from django.conf.urls.defaults import patterns, url

from views import get_ueditor_controller

urlpatterns = patterns('',
    url(r'^controller/$',get_ueditor_controller)
)