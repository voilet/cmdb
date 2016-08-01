# coding:utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
import re
import sys
import time
from datetime import datetime

reload(sys)
sys.setdefaultencoding('utf8')

from pyzabbix import ZabbixAPI

from django.shortcuts import get_object_or_404

from mysite.settings import zabbix_url, zabbix_user, zabbix_passwd
from assets.models import IDC, Host, Project, Service, ZabbixRecord
from mysite.settings import zabbix_on



zapi = ZabbixAPI(zabbix_url)

if zabbix_on:
    zapi.login(zabbix_user, zabbix_passwd)

zabbix_agent_port = 10050
fun_linux_base_id = 10105


def db_zabbix(name, type, ret):
    """ zabbix插入添加记录 """
    print name, type, ret
    ZabbixRecord.objects.create(name=name, type=type, status=ret)


def zabbix_host_add(request):
    """ zabbix添加主机 """
    node_name = request.POST.get('node_name', '')
    project_uuid = request.POST.getlist('business', '')
    eth1 = request.POST.get('eth1', '')
    service_uuid = request.POST.getlist('service', '')
    idc_uuid = request.POST.get('idc', '')
    idc = get_object_or_404(IDC, uuid=idc_uuid)
    idc_name = idc.name

    zabbix_info = zapi.host.get(filter=({'host': eth1}))
    if len(zabbix_info) != 0:
        ret = 2
    else:
        project_name, service_name, template_list = [], [], []
        for uuid in project_uuid:
            name = get_object_or_404(Project, uuid=uuid).service_name
            project_name.append(name)

        for uuid in service_uuid:
            service = get_object_or_404(Service, uuid=uuid)
            template_name = service.name + '_' + str(service.port)
            template_list.append(template_name)
            service_name.append(service.name)

        zabbix_group_id, zabbix_template_id = [], [fun_linux_base_id]
        groups_list, templates_list = [], [{'templateid': fun_linux_base_id}]
        zabbix_group = zapi.hostgroup.get(filter=({'name': project_name}))
        for group in zabbix_group:
            group_id = group.get('groupid')
            zabbix_group_id.append(int(group_id))
            groups_list.append({'groupid': int(group_id)})

        zabbix_template = zapi.template.get(filter=({'host': template_list}))
        for template in zabbix_template:
            template_id = template.get('templateid')
            zabbix_template_id.append(int(template_id))
            templates_list.append({'templateid': int(template_id)})

        if idc.get_type_display() == 'CDN':
            zabbix_name = str(idc_name + '_' + service_name[0] + '_' + eth1)

            group_idc_id = zapi.hostgroup.get(filter=({'name': idc_name}))[0].get('groupid')
            zabbix_group_id.append(int(group_idc_id))
            groups_list.append({'groupid': int(group_idc_id)})
        else:
            zabbix_name = str(idc_name + '_' + project_name[0] + '_' + service_name[0] + '_' + eth1)

        zabbix_host = zabbix_ip = str(eth1)
        host_info = {'host': zabbix_host,
                     'name': zabbix_name,
                     'interfaces': [{'type': 1,
                                     'main': 1,
                                     'useip': 1,
                                     'ip': zabbix_ip,
                                     'dns': '',
                                     'port': zabbix_agent_port}],
                     'groups': groups_list,
                     'templates': templates_list}
        print node_name, zabbix_ip, zabbix_name, zabbix_group_id, zabbix_template_id
        print host_info
        zapi.host.create(host_info)
        ret = 1
    db_zabbix(eth1, u'主机', ret)
    return ret


def zabbix_group_add(name):
    """ zabbix添加主机组 """
    zabbix_info = zapi.hostgroup.get(filter=({'name': name}))
    if len(zabbix_info) != 0:
        ret = 0
    else:
        group_info = {'name': name}
        zapi.hostgroup.create(group_info)
        ret = 1
    return ret


def zabbix_group_del(name):
    """ zabbix删除主机组 """
    zabbix_info = zapi.hostgroup.get(filter=({'name': name}))
    if len(zabbix_info) == 0:
        ret = 0
    else:
        groupid = zabbix_info[0].get('groupid')
        zapi.hostgroup.delete(groupid)
        ret = 1
    return ret


def zabbix_template_add(request):
    """ zabbix添加模板 """
    service_name = request.POST.get('name')
    service_port = request.POST.get('port')
    template_name = service_name + '_' + str(service_port)
    item_name = 'tcp_' + str(service_port)
    zabbix_info = zapi.template.get(filter=({'name': template_name}))
    if len(zabbix_info) != 0:
        ret = 0
    else:
        template_info = {'host': template_name,
                         'groups': {'groupid': 1}}
        print template_info
        zapi.template.create(template_info)
        templateid = zapi.template.get(filter=({'name': template_name}))[0].get('templateid')
        item_info = {'name': item_name,
                     'hostid': templateid,
                     'key_': 'net.tcp.port[,%s]' % service_port,
                     'type': 0,
                     'value_type': 3,
                     'delay': 30}
        zapi.item.create(item_info)
        trigger_info = {"description": "%s port %s is down on {HOST.NAME}" % (service_name, service_port),
                        "expression": "{%s:net.tcp.port[,%s].last()}<>1" % (template_name, service_port)}
        zabbix_trigger_add(trigger_info)
        ret = 1
    return ret


def zabbix_item_add(zabbix_info):
    zapi.item.create(zabbix_info)


def zabbix_trigger_add(zabbix_info):
    zapi.trigger.create(zabbix_info)


def zabbix_get_graph(ip):
    """ 获取主机图形ip """
    hostid = zapi.host.get(filter=({'host': ip}))[0]['hostid']
    host_info = {'hostid': hostid, 'output': 'extend'}
    graph_ids = {}
    zabbix_graph = zapi.graph.get(filter=host_info)
    for graph in zabbix_graph:
        graph_id = int(graph['graphid'])
        graph_name = graph['name']
        graph_ids[graph_name] = graph_id
    return graph_ids


def zabbix_get_item(ip):
    """ 获取主机监控项目 """
    pattern1 = re.compile(r'.*\[(.*)\].*')
    pattern2 = re.compile(r'.*\[(/.*),.*\]')
    pattern3 = re.compile(r'.*\[,(.*)\].*')
    host = zapi.host.get(filter=({'host': ip}))
    if not host:
        return False
    hostid = host[0]['hostid']
    host_info = {'hostid': hostid, 'output': 'extend'}
    item_info = []
    zabbix_item = zapi.item.get(filter=host_info)
    for item in zabbix_item:
        item_name = item.get('name')
        item_key = item.get('key_')
        if 'network traffic on' in item_name:
            match = pattern1.match(item_key)
            if match:
                interface = match.groups()[0]
                item_name = item_name.replace('$1', interface)
        if 'Free' in item_name:
            match = pattern2.match(item_key)
            if match:
                disk = match.groups()[0]
                item_name = item_name.replace('$1', disk)
        if 'CPU $2 time' in item_name:
            match = pattern3.match(item_key)
            if match:
                cpu_type = match.groups()[0]
                item_name = item_name.replace('$2', cpu_type)
        item_info.append(item_name)

    return item_info


def zabbix_get_trigger(ip):
    """ 获取主机trigger """
    host = zapi.host.get(filter=({'host': ip}))
    if not host:
        return False
    hostid = host[0]['hostid']
    host_info = {'hostid': hostid, 'output': 'extend'}
    host_trigger = zapi.trigger.get(filter=host_info)
    trigger_info = {}
    for trigger in host_trigger:
        t_value = int(trigger.get('value'))
        if t_value == 1:
            t_time = int(trigger.get('lastchange'))
            t_des = trigger.get('description')
            t_time = datetime.fromtimestamp(t_time)
            trigger_info[t_time] = t_des

    return trigger_info


def zabbix_get_alert_bak(ip):
    """ 获取主机告警历史 """
    hostid = zapi.host.get(filter=({'host': ip}))[0]['hostid']
    host_info = {'hostid': hostid, 'output': 'extend'}
    host_alert = zapi.alert.get(filter=host_info)
    alert_info = []
    for alert in host_alert:
        t_time = alert.get('clock')
        t_message = alert.get('message')

        time_now = time.time()
        time_interval = int(time_now) - int(t_time)
        if time_interval < 86400:
            x = time.localtime(int(t_time))
            t_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
            alert_info.append((t_time, t_message))
    alert_info.reverse()

    return alert_info


def zabbix_get_alert(ip):
    print datetime.utcnow()
    trigger_id, event_id, alert_info = [], [], []
    time_till = int(time.time())
    time_from = time_till - 86400
    hostid = zapi.host.get(filter=({'host': ip}))[0]['hostid']
    host_info = {'hostid': hostid, 'output': 'extend'}
    host_trigger = zapi.trigger.get(filter=host_info)
    for trigger in host_trigger:
        trigger_id.append(trigger.get('triggerid'))
    for id in trigger_id:
        trigger_info = {'output': 'extend',
                        "select_acknowledges": "extend",
                        "objectid": id,
                        "sortorder": "DESC"}
        host_event = zapi.event.get(filter=trigger_info)
        for event in host_event:
            event_id.append(event.get('eventid'))

    for id in event_id:
        alerts_info = {"output": "extend", "eventid": id}
        host_alert = zapi.alert.get(filter=alerts_info)
        for alert in host_alert:
            message = alert.get('message')
            sendto = alert.get('sendto')
            clock = alert.get('clock')
            if int(clock) > time_from:
                x = time.localtime(int(clock))
                clock = time.strftime('%Y-%m-%d %H:%M:%S', x)
                alert_info.append((clock, sendto, message))
    alert_info.reverse()
    print datetime.utcnow()
    return alert_info




def zabbix_get_item_count(ip):
    """ 获取主机监控项目 """
    if zabbix_on:
        host = zapi.host.get(filter=({'host': ip}))
        if not host:
            return False
        hostid = host[0]['hostid']
        host_info = {'hostid': hostid, 'output': 'extend'}
        zabbix_item = len(zapi.item.get(filter=host_info))
        return zabbix_item
    else:
        zabbix_item = ""
        return zabbix_item


def zabbix_get_trigger_count(ip):
    """ 获取主机trigger """
    i = 0
    if zabbix_on:
        host = zapi.host.get(filter=({'host': ip}))
        if not host:
            return False
        hostid = host[0]['hostid']
        host_info = {'hostid': hostid, 'output': 'extend'}
        host_trigger = zapi.trigger.get(filter=host_info)
        for trigger in host_trigger:
            t_value = int(trigger.get('value'))
            if t_value == 1:
                i += 1

        return i
    return