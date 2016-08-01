# coding:utf-8
from assets.views import salt_record, db_to_record
from assets.models import Host, IDC
from assets.zabbix import *
from mysite.settings import salt_cdn_url, salt_center_url, salt_user, salt_passwd
from assets.new_api import SaltApi

from django.http import HttpResponseRedirect


def host_update(host):
    """ 使用salt更新资产信息 """
    hostname = str(host.node_name)
    idc_type = host.idc.get_type_display()
    if idc_type == 'CDN':
        salt_url = salt_cdn_url
    elif idc_type == '核心':
        salt_url = salt_center_url
    salt_api = SaltApi(url=salt_url, username=salt_user, password=salt_passwd)
    grains = salt_api.remote_noarg_exec(hostname, 'grains.items')
    if len(grains) == 0:
        print 'no grains'
        return False
    ip_info = grains['ip_interfaces']
    mac_info = grains['hwaddr_interfaces']
    if 'eth0' in ip_info:
        if 'bond0' in ip_info:
            eth1 = ip_info['bond0'][0]
            mac = mac_info["bond0"]
        elif 'br0' in ip_info:
            eth1 = ip_info['br0'][0]
            mac = mac_info["br0"]
        else:
            eth1 = ip_info["eth0"][0]
            mac = mac_info['eth0']
    elif 'em1' in ip_info:
        if 'bond0' in ip_info:
            try:
                eth1 = ip_info['bond0'][0]
            except Exception as e:
                eth1 = ''
            mac = mac_info["bond0"]

        elif 'br0' in ip_info:
            try:
                eth1 = ip_info['br0'][0]
            except Exception as e:
                eth1 = ''
            mac = mac_info["br0"]
        else:
            eth1 = ip_info["em1"][0]
            mac = mac_info["em1"]
    else:
        eth1 = "127.0.0.1"

    system = grains['os']
    system_cpuarch = grains['osarch']
    server_sn = grains['sn']
    system_version = grains['osrelease']
    cpu = grains['cpu_model'].split()[3] + '*' + str(grains['num_cpus'])
    hard_disk = grains['disk']
    memory = grains['memory']
    brand = grains['brand']
    salt_data = {'eth1': eth1, 'mac': mac, 'system': system, 'system_cpuarch': system_cpuarch,
                 'server_sn': server_sn, 'system_version': system_version, 'cpu': cpu,
                 'hard_disk': hard_disk, 'memory': memory, 'brand': brand}
    info = salt_record(host, salt_data)
    db_to_record('salt', host, info)
    host.eth1 = eth1
    host.mac = mac
    host.cpu = cpu
    host.hard_disk = hard_disk
    host.memory = memory
    host.brand = brand
    host.system = system
    host.system_cpuarch = system_cpuarch
    host.system_version = system_version
    host.server_sn = server_sn
    host.save()


def zabbix_host_add(host):
    """ zabbix添加主机 """
    eth1 = host.eth1
    node_name = host.node_name
    idc = host.idc
    idc_name = host.idc.name
    projects = host.business.all()
    services = host.service.all()
    zabbix_info = zapi.host.get(filter=({'host': eth1}))
    if len(zabbix_info) != 0:
        ret = 2
    else:
        project_name, service_name, template_list = [], [], []
        for p in projects:
            name = p.service_name
            project_name.append(name)

        for service in services:
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


def test_bak(request):
    idc_name = '福建移动'
    idc = IDC.objects.get(name=idc_name)

    host_all = Host.objects.filter(idc=idc)
    for host in host_all:
        print host
        host_update(host)
    return HttpResponseRedirect('/')


def test(request):
    # host = Host.objects.get(eth1='117.34.78.5')
    # zabbix_host_add(host)
    idc_name = '郑州联通'
    idc = IDC.objects.get(name=idc_name)
    host_all = Host.objects.filter(idc=idc)
    for host in host_all:
        print host
        zabbix_host_add(host)
    return HttpResponseRedirect('/')