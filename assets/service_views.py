# coding:utf-8
import ast
from django.http import HttpResponseRedirect
from assets.models import Host, IDC, Service
from django.shortcuts import get_object_or_404
from assets.forms import ServiceForm
from assets.views import my_render
from assets.zabbix import zabbix_template_add
from mysite.settings import zabbix_on


def service_add(request):
    """ 添加服务 """
    sf = ServiceForm()
    if request.method == 'POST':
        sf_post = ServiceForm(request.POST)
        print 'ok'
        if sf_post.is_valid():
            print 'ok2'
            service_port = sf_post.cleaned_data.get('port')
            print service_port
            sf_post.save()
            if zabbix_on and service_port:
                ret = zabbix_template_add(request)
            return HttpResponseRedirect('/assets/service_list/')
    return my_render('assets/service_add.html', locals(), request)


def service_list(request):
    """ 列出服务 """
    services = Service.objects.all()
    return my_render('assets/service_list.html', locals(), request)


def service_edit(request):
    """ 编辑服务 """
    uuid = request.GET.get('uuid', '')
    service = get_object_or_404(Service, uuid=uuid)
    if request.method == 'POST':
        sf = ServiceForm(request.POST, instance=service)
        if sf.is_valid():
            sf.save()
            return HttpResponseRedirect("/assets/service_list/")
    else:
        sf = ServiceForm(instance=service)
        return my_render('assets/service_edit.html', locals(), request)


def service_del(request):
    """ 删除服务 """
    uuid = request.GET.get('uuid')
    if uuid:
        service = get_object_or_404(Service, uuid=uuid)
        service.host_set.clear()
        service.delete()
        return HttpResponseRedirect('/assets/service_list/')
