# coding:utf-8
import ast
import nmap

from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from assets.models import Host, IDC, Service, Line, Project, HostRecord
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from forms import HostForm, IdcForm
from new_api import SaltApi, pages, sort_ip_list, get_mask_ip
from mysite.settings import salt_cdn_url, salt_center_url, salt_user, salt_passwd, zabbix_on
from assets.models import SERVER_STATUS, Server_System, ZabbixRecord, IpList
from zabbix import zabbix_host_add, zabbix_group_add, zabbix_group_del, zabbix_get_graph, zabbix_get_item, \
    zabbix_get_trigger, zabbix_get_alert
from pdf import rpt, excel_output
from assets.models import Project
from assets.forms import Project_docForm
from django.http import HttpResponse


class RaiseError(Exception):
    pass


def my_render(template, data, request):
    return render_to_response(template, data, context_instance=RequestContext(request))


@login_required
def httperror(request, emg):
    message = emg
    return render_to_response('error.html', locals())


def get_diff(obj1, obj2):
    fields = ['service', 'business']
    no_check_fields = ['cpu', 'core_num', 'hard_disk', 'memory']
    d1, d2 = obj1, dict(obj2.iterlists())
    info = {}
    for k, v in d1.items():
        if k in fields:
            if d2.get(k):
                d2_value = d2[k]
            else:
                d2_value = u''
        elif k in no_check_fields:
            continue
        else:
            d2_value = d2[k][0]
        if not v:
            v = u''
        if str(v) != str(d2_value):
            info.update({k: [v, d2_value]})

    for k, v in info.items():
        if v == [None, u'']:
            info.pop(k)
    return info


def db_to_record(username, host, info):
    text_list = []
    for k, v in info.items():
        field = Host._meta.get_field_by_name(k)[0].verbose_name
        if k == 'idc':
            old = IDC.objects.filter(uuid=v[0])
            new = IDC.objects.filter(uuid=v[1])
            if old:
                name_old = old[0].name
            else:
                name_old = u'无'
            if new:
                name_new = new[0].name
            else:
                name_new = u'无'
            text = field + u'由 ' + name_old + u' 更改为 ' + name_new

        elif k == 'service':
            old, new = [], []
            for s in v[0]:
                service_name = Service.objects.get(uuid=s).name
                old.append(service_name)
            for s in v[1]:
                service_name = Service.objects.get(uuid=s).name
                new.append(service_name)
            text = field + u'由 ' + ','.join(old) + u' 更改为 ' + ','.join(new)

        elif k == 'business':
            old, new = [], []
            for s in v[0]:
                project_name = Project.objects.get(uuid=s).service_name
                old.append(project_name)
            for s in v[1]:
                project_name = Project.objects.get(uuid=s).service_name
                new.append(project_name)
            text = field + u'由 ' + ','.join(old) + u' 更改为 ' + ','.join(new)

        elif k == 'vm':
            old = Host.objects.filter(uuid=v[0])
            new = Host.objects.filter(uuid=v[1])
            if old:
                name_old = old[0].eth1
            else:
                name_old = u'无'
            if new:
                name_new = new[0].eth1
            else:
                name_new = u'无'
            text = field + u'父主机由 ' + name_old + u' 更改为 ' + name_new

        else:
            text = field + u'由 ' + str(v[0]) + u' 更改为 ' + str(v[1])
        text_list.append(text)

    if len(text_list) != 0:
        HostRecord.objects.create(host=host, user=username, content=text_list)


def salt_record(host, salt_data):
    """ salt更新资产添加历史记录 """
    info = {}
    field_list = ['eth1', 'mac', 'system', 'system_cpuarch', 'server_sn',
                  'system_version', 'cpu', 'core_num', 'hard_disk', 'memory', 'brand']
    host_dic = host.__dict__
    for field in field_list:
        old = host_dic.get(field)
        new = salt_data.get(field)
        if old != new:
            info[field] = [old, new]
    return info


@login_required
def host_add(request):
    """ 添加主机 """
    uf = HostForm()
    projects = Project.objects.all()
    services = Service.objects.all()

    if request.method == 'POST':
        uf_post = HostForm(request.POST)
        physics = request.POST.get('physics', '')
        ip = request.POST.get('eth1', '')
        if Host.objects.filter(eth1=ip):
            emg = u'添加失败, 该IP %s 已存在!' % ip
            return my_render('assets/host_add.html', locals(), request)
        if uf_post.is_valid():
            zw = uf_post.save(commit=False)
            zw.mac = str(request.POST.getlist("mac")[0]).replace(':', '-').strip(" ")
            status = uf_post.cleaned_data['status']
            if physics:
                physics_host = get_object_or_404(Host, eth1=physics)
                zw.vm = physics_host
                zw.type = 1
            else:
                zw.type = 0
            zw.save()
            uf_post.save_m2m()
            if zabbix_on and status == 1:
                zabbix_host_add(request)
            smg = u'主机%s添加成功!' % ip
            return render_to_response('assets/host_add.html', locals(), context_instance=RequestContext(request))

    return render_to_response('assets/host_add.html', locals(), context_instance=RequestContext(request))


@login_required
def host_edit(request):
    """ 修改主机 """
    uuid = request.GET.get('uuid')
    host = get_object_or_404(Host, uuid=uuid)
    uf = HostForm(instance=host)
    project_all = Project.objects.all()
    project_host = host.business.all()
    projects = [p for p in project_all if p not in project_host]

    service_all = Service.objects.all()
    service_host = host.service.all()
    services = [s for s in service_all if s not in service_host]
    username = request.user.username
    if request.method == 'POST':
        physics = request.POST.get('physics', '')
        uf_post = HostForm(request.POST, instance=host)
        if uf_post.is_valid():
            zw = uf_post.save(commit=False)
            zw.mac = str(request.POST.getlist("mac")[0]).replace(':', '-').strip(" ")
            request.POST = request.POST.copy()
            if physics:
                physics_host = get_object_or_404(Host, eth1=physics)
                request.POST['vm'] = physics_host.uuid
                if host.vm:
                    if str(host.vm.eth1) != str(physics):
                        zw.vm = physics_host
                else:
                    zw.vm = physics_host
                zw.type = 1
            else:
                request.POST['vm'] = ''
                zw.type = 0

            zw.save()
            uf_post.save_m2m()
            new_host = get_object_or_404(Host, uuid=uuid)
            info = get_diff(uf_post.__dict__.get('initial'), request.POST)
            db_to_record(username, host, info)
            return HttpResponseRedirect('/assets/host_detail/?uuid=%s' % uuid)

    return render_to_response('assets/host_edit.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_exempt
def host_edit_batch(request):
    """ 批量修改主机 """
    uf = HostForm()
    username = request.user.username
    projects = Project.objects.all()
    services = Service.objects.all()
    if request.method == 'POST':
        ids = str(request.GET.get('uuid', ''))
        env = request.POST.get('env', '')
        idc = request.POST.get('idc', '')
        brand = request.POST.get('brand', '')
        business = request.POST.getlist('business', '')
        services = request.POST.getlist('service', '')
        cabinet = request.POST.get('cabinet', '')
        editor = request.POST.get('editor', '')
        uuid_list = ids.split(",")

        for uuid in uuid_list:
            record_list = []
            host = get_object_or_404(Host, uuid=uuid)
            if env:
                if not host.env:
                    info = u'无'
                else:
                    info = host.env
                if env != host.env:
                    text = u'环境' + u'由 ' + info + u' 更改为 ' + env
                    record_list.append(text)
                    host.env = env

            if idc:
                get_idc = get_object_or_404(IDC, uuid=idc)

                if host.idc != get_idc.name:
                    if not host.idc:
                        text = u'IDC' + u'由 ' + "none" + u' 更改为 ' + get_idc.name
                    else:
                        text = u'IDC' + u'由 ' + host.idc.name + u' 更改为 ' + get_idc.name
                    record_list.append(text)
                    host.idc = get_idc

            if brand:
                if brand != host.brand:
                    text = u'硬件厂商' + u'由 ' + host.brand + u' 更改为 ' + brand
                    record_list.append(text)
                    host.brand = brand

            if business:
                old, new, project_list = [], [], []
                for s in host.business.all():
                    project_name = s.service_name
                    old.append(project_name)
                for s in business:
                    project = Project.objects.get(uuid=s)
                    project_name = project.service_name
                    new.append(project_name)
                    project_list.append(project)
                if old != new:
                    text = u'所属业务' + u'由 ' + ','.join(old) + u' 更改为 ' + ','.join(new)
                    record_list.append(text)
                    host.business = project_list

            if services:
                old, new, service_list = [], [], []
                for s in host.service.all():
                    service_name = s.name
                    old.append(service_name)
                for s in services:
                    service = Service.objects.get(uuid=s)
                    service_name = service.name
                    new.append(service_name)
                    service_list.append(service)
                if old != new:
                    text = u'运行服务' + u'由 ' + ','.join(old) + u' 更改为 ' + ','.join(new)
                    record_list.append(text)
                    host.service = service_list

            if cabinet:
                if not host.cabinet:
                    info = u'无'
                else:
                    info = host.cabinet
                if cabinet != host.cabinet:
                    text = '机柜号' + u'由 ' + info + u' 更改为 ' + cabinet
                    record_list.append(text)
                    host.cabinet = cabinet

            if editor:
                if editor != host.editor:
                    text = '备注' + u'由 ' + host.editor + u' 更改为 ' + editor
                    record_list.append(text)
                    host.editor = editor

            if len(record_list) != 0:
                host.save()
                HostRecord.objects.create(host=host, user=username, content=record_list)

        return my_render('assets/host_edit_batch_ok.html', locals(), request)
    return my_render('assets/host_edit_batch.html', locals(), request)


@login_required
def host_detail(request):
    """ 主机详情 """
    uuid = request.GET.get('uuid', '')
    ip = request.GET.get('ip', '')
    if uuid:
        host = get_object_or_404(Host, uuid=uuid)
    elif ip:
        host = get_object_or_404(Host, eth1=ip)
    host_record = HostRecord.objects.filter(host=host).order_by('-time')
    return render_to_response('assets/host_detail.html', locals(), context_instance=RequestContext(request))


@login_required
def host_del(request):
    """ 删除主机 """
    uuid = request.GET.get('uuid', '')
    host = get_object_or_404(Host, uuid=uuid)
    host.status = 3
    host.eth1 = ''
    host.eth2 = ''
    host.node_name = host.uuid
    host.internal_ip = ''
    host.system = ''
    host.system_cpuarch = ''
    host.system_version = ''
    host.cabinet = ''
    host.server_cabinet_id = 0
    host.env = ''
    host.number = ''
    host.switch_port = ''
    host.idc = IDC.objects.get(name=u"报废库房")
    host.business.clear()
    host.service.clear()
    host.save()
    return HttpResponseRedirect('/assets/host_list/')


@login_required
def host_del_batch(request):
    """ 批量删除主机 """
    ids = str(request.POST.get('ids'))
    for uuid in ids.split(','):
        host = get_object_or_404(Host, uuid=uuid)
        host.status = 3
        host.eth1 = ''
        host.eth2 = ''
        host.node_name = host.uuid
        host.internal_ip = ''
        host.system = ''
        host.system_cpuarch = ''
        host.system_version = ''
        host.cabinet = ''
        host.server_cabinet_id = 0
        host.env = ''
        host.number = ''
        host.switch_port = ''
        host.idc = IDC.objects.get(name=u'报废库房')
        host.business.clear()
        host.service.clear()
        host.save()
    return HttpResponseRedirect('/assets/host_list/')


@login_required
def host_list(request):
    """ 主机列表 """
    hosts = Host.objects.all().order_by("-eth1")
    idcs = IDC.objects.filter()
    lines = Line.objects.all()
    server_type = Project.objects.all()
    services = Service.objects.all()
    brands = Server_System
    server_status = SERVER_STATUS
    server_list_count = hosts.count()
    physics = Host.objects.filter(vm__isnull=True).count()
    vms = Host.objects.filter(vm__isnull=False).count()
    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(hosts, request)

    return render_to_response('assets/host_list.html', locals(), context_instance=RequestContext(request))


@login_required
@csrf_protect
def host_add_batch_bak(request):
    """ 批量添加主机 """
    if request.method == 'POST':
        multi_hosts = request.POST.get('batch').split('\n')
        for host in multi_hosts:
            if host == '':
                break
            ip, hostname, idc, service, brand, comment, pip = host.split()
            idc = get_object_or_404(IDC, name=idc)
            services = []
            for s in ast.literal_eval(service):
                services.append(get_object_or_404(Service, name=s.strip()))

            if Host.objects.filter(eth1=ip):
                emg = u'添加失败, 该IP%s已存在' % ip
                return my_render('assets/host_add_batch.html', locals(), request)

            if pip != '[]':
                pip = Host.objects.get(eth1=ast.literal_eval(pip)[0])
                asset = Host(node_name=hostname, eth1=ip, idc=idc, brand=brand, editor=comment, vm=pip)
            else:
                asset = Host(node_name=hostname, eth1=ip, idc=idc, brand=brand, editor=comment)
            asset.save()
            asset.service = services
            asset.save()
        smg = u'批量添加成功.'
        return my_render('assets/host_add_batch.html', locals(), request)

    return my_render('assets/host_add_batch.html', locals(), request)


@login_required
@csrf_protect
def host_add_batch(request):
    """ 批量添加主机 """
    if request.method == 'POST':
        multi_hosts = request.POST.get('batch').split('\n')
        for host in multi_hosts:
            if host == '':
                break
            number, brand, hard_info, eth1, eth2, internal_ip, idc, comment = host.split('!@')
            hard_info = ast.literal_eval(hard_info)
            cpu, memory, hard_disk = hard_info[0:3]
            idc = IDC.objects.get(name=idc)
            asset = Host(number=number, brand=brand, idc=idc, cpu=cpu,
                         memory=memory, hard_disk=hard_disk, eth1=eth1,
                         eth2=eth2, internal_ip=internal_ip, editor=comment)
            asset.save()
        smg = u'批量添加成功.'
        return my_render('assets/host_add_batch.html', locals(), request)

    return my_render('assets/host_add_batch.html', locals(), request)


@login_required
def idc_add(request):
    """ 添加IDC """
    if request.method == 'POST':
        init = request.GET.get("init", False)

        uf = IdcForm(request.POST)
        if uf.is_valid():
            idc_name = uf.cleaned_data['name']
            if IDC.objects.filter(name=idc_name):
                emg = u'添加失败, 此IDC %s 已存在!' % idc_name
                return my_render('assets/idc_add.html', locals(), request)
            uf.save()
            if zabbix_on:
                ret = zabbix_group_add(idc_name)
                if ret != 1:
                    emg = u'添加zabbix主机组 %s 失败!' % idc_name
                    return my_render('assets/idc_add.html', locals(), request)
            if not init:
                return HttpResponseRedirect("/assets/idc_list/")
            else:
                return HttpResponseRedirect('/assets/server/type/add/?init=true')

    else:
        uf = IdcForm()
    return render_to_response('assets/idc_add.html', locals(), context_instance=RequestContext(request))


@login_required
def idc_list(request):
    idcs = IDC.objects.all()
    server_type = Project.objects.all()
    return render_to_response('assets/idc_list.html', locals(), context_instance=RequestContext(request))


@login_required
def idc_edit(request):
    uuid = request.GET.get('uuid', '')
    idc = get_object_or_404(IDC, uuid=uuid)
    if request.method == 'POST':
        uf = IdcForm(request.POST, instance=idc)
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect("/assets/idc_list/")
    else:
        uf = IdcForm(instance=idc)
        return my_render('assets/idc_edit.html', locals(), request)


@login_required
def idc_del(request):
    uuid = request.GET.get('uuid', '')
    idc = get_object_or_404(IDC, uuid=uuid)
    idc_name = idc.name
    if zabbix_on:
        zabbix_group_del(idc_name)
    idc.delete()
    return HttpResponseRedirect('/assets/idc_list/')


@login_required
@csrf_exempt
def host_search(request):
    """ 条件搜索ajax """

    idcs = IDC.objects.filter()
    lines = Line.objects.all()
    server_type = Project.objects.all()
    services = Service.objects.all()
    brands = Server_System
    server_status = SERVER_STATUS

    lines = Line.objects.all()
    businesses = Project.objects.all()
    idc_name = request.GET.get('change_idc', '')
    business_name = request.GET.get('change_business', '')
    service_name = request.GET.get('change_service', '')
    brand_name = request.GET.get('change_brand', '')
    if brand_name:
        brand_name = brand_name
    status = request.GET.get('change_status', False)
    if status:
        status = int(status)
    else:
        status = ""

    type = request.GET.get('change_type', '')

    if not idc_name and not type and not status and not brand_name and business_name == 'all' \
            and service_name == 'all':
        select_number = 0
    else:
        select_number = 1

    keyword = request.GET.get('keyword', '')
    s_url = request.get_full_path()

    if business_name == 'all' and service_name != 'all':
        ser = Service.objects.get(name=service_name)
        hosts = Host.objects.filter(idc__name__contains=idc_name,
                                    service=ser,
                                    brand__contains=brand_name,
                                    status__contains=status,
                                    type__contains=type)

    elif service_name == 'all' and business_name != 'all':
        business = Project.objects.get(service_name=business_name)
        hosts = Host.objects.filter(idc__name__contains=idc_name,
                                    business=business,
                                    brand__contains=brand_name,
                                    status__contains=status,
                                    type__contains=type)

    elif business_name == 'all' and service_name == 'all':
        hosts = Host.objects.filter(idc__name__contains=idc_name,
                                    brand__contains=brand_name,
                                    status__contains=status,
                                    type__contains=type)

    else:
        ser = Service.objects.get(name=service_name)
        business = Project.objects.get(service_name=business_name)
        hosts = Host.objects.filter(idc__name__contains=idc_name,
                                    business=business,
                                    service=ser,
                                    brand__contains=brand_name,
                                    status__contains=status,
                                    type__contains=type)

    if keyword and select_number == 1:
        hosts = hosts.filter(Q(node_name__contains=keyword) |
                             Q(idc__name__contains=keyword) |
                             Q(eth1__contains=keyword) |
                             Q(eth2__contains=keyword) |
                             Q(internal_ip__contains=keyword) |
                             Q(brand__contains=keyword) |
                             Q(number__contains=keyword) |
                             Q(editor__contains=keyword) |
                             Q(business__service_name__contains=keyword) |
                             Q(service__name__contains=keyword) |
                             Q(Services_Code__contains=keyword) |
                             Q(server_sn__contains=keyword) |
                             Q(cpu__contains=keyword) |
                             Q(memory__contains=keyword) |
                             Q(hard_disk__contains=keyword))

    elif keyword:
        hosts = Host.objects.filter(Q(node_name__contains=keyword) |
                                    Q(idc__name__contains=keyword) |
                                    Q(eth1__contains=keyword) |
                                    Q(eth2__contains=keyword) |
                                    Q(internal_ip__contains=keyword) |
                                    Q(brand__contains=keyword) |
                                    Q(number__contains=keyword) |
                                    Q(editor__contains=keyword) |
                                    Q(business__service_name__contains=keyword) |
                                    Q(service__name__contains=keyword) |
                                    Q(Services_Code__contains=keyword) |
                                    Q(server_sn__contains=keyword) |
                                    Q(cpu__contains=keyword) |
                                    Q(memory__contains=keyword) |
                                    Q(hard_disk__contains=keyword))

    hosts = list(set(hosts))
    hosts_dic = {}
    hosts_lis = []
    for host in hosts:
        if host.eth1:
            hosts_dic[host.eth1] = host
            hosts_lis.append(host.eth1)
        elif host.eth2:
            hosts_dic[host.eth2] = host
            hosts_lis.append(host.eth2)
    sort_ip_list(hosts_lis)
    hosts = []
    for eth1 in hosts_lis:
        hosts.append(hosts_dic[eth1])

    search_status = request.GET.get("_search", False)
    search_output_name = request.GET.get("name", False)
    if search_status and search_output_name:
        if search_output_name == 'pdf':
            s = rpt(hosts)
            if s:
                data = "pdf"
                return render_to_response('assets/download.html', locals(), context_instance=RequestContext(request))

        if search_output_name == 'excel':
            s = excel_output(hosts)
            if s:
                data = "execl"
                return render_to_response('assets/download.html', locals(), context_instance=RequestContext(request))

    contact_list, p, contacts, page_range, current_page, show_first, show_end = pages(hosts, request)

    if 'ajax' in request.get_full_path():
        s_url = s_url.replace('change_info_ajax', 'host_search')
        return my_render('assets/host_info_ajax.html', locals(), request)
    else:
        hosts = Host.objects.all()
        idcs = IDC.objects.filter()
        lines = Line.objects.all()
        server_type = Project.objects.all()
        services = Service.objects.all()
        brands = Server_System
        server_status = SERVER_STATUS
        server_list_count = hosts.count()
        physics = Host.objects.filter(vm__isnull=True).count()
        vms = Host.objects.filter(vm__isnull=False).count()
        search = 1
        return my_render('assets/host_list.html', locals(), request)


@login_required
def host_update(request):
    """ 使用salt更新资产信息 """
    uuid = request.GET.get('uuid', '')
    host = get_object_or_404(Host, uuid=uuid)
    hostname = str(host.node_name)
    idc_type = host.idc.get_type_display()
    if idc_type == 'CDN':
        salt_url = salt_cdn_url
    elif idc_type == '核心':
        salt_url = salt_center_url
    salt_api = SaltApi(url=salt_url, username=salt_user, password=salt_passwd)
    grains = salt_api.remote_noarg_exec(hostname, 'grains.items')
    if len(grains) == 0:
        return httperror(request, '此主机salt-minion无数据返回, 请确定minion是否正常运行.')
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
            eth1 = ip_info['bond0'][0]
            mac = mac_info["bond0"]
        elif 'br0' in ip_info:
            eth1 = ip_info['br0'][0]
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

    return HttpResponseRedirect('/assets/host_detail/?uuid=%s' % uuid)


@login_required
def zabbix_info(request):
    """ zabbix信息 """
    records = ZabbixRecord.objects.all()
    return my_render('assets/zabbix.html', locals(), request)


@login_required
def zabbix_host(request):
    """ zabbix主机详情页 """
    uuid = request.GET.get('uuid')
    host = get_object_or_404(Host, uuid=uuid)
    eth1 = host.eth1
    graphs = zabbix_get_graph(eth1)
    items = zabbix_get_item(eth1)
    triggers = zabbix_get_trigger(eth1)
    alerts = zabbix_get_alert(eth1)
    return my_render('assets/zabbix_host.html', locals(), request)


@login_required
def ip_list(request):
    """ ip列表 """
    idcs = IDC.objects.all()
    yizhuang_idc = get_object_or_404(IDC, name='亦庄电信')
    active_111 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.111.0/24', status=1)
    unactive_111 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.111.0/24', status=1)
    active_112 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.112.0/24', status=1)
    unactive_112 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.112.0/24', status=1)
    active_113 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.113.0/24', status=1)
    unactive_113 = IpList.objects.filter(idc=yizhuang_idc, network='192.168.113.0/24', status=1)
    return my_render('assets/ip_list.html', locals(), request)


@login_required
def ip_list_ajax(request):
    """ ip网段异步 """
    idc_name = request.GET.get('idc_name', '')
    idc = get_object_or_404(IDC, name=idc_name)
    if idc:
        network = idc.network
        if network:
            networks = network.split('\r\n')
        else:
            networks = [u'无']
    return my_render('assets/ip_list_ajax.html', locals(), request)


@login_required
def ip_list_info(request):
    """"""
    idc_name = request.GET.get('idc_name', '')
    network = request.GET.get('network', '')
    fresh = request.GET.get('fresh', '')
    idc = get_object_or_404(IDC, name=idc_name)
    if fresh == '1':
        ip_active, ip_unactive = ip_list_refresh(idc, network)
    elif fresh == '0':
        ip_active = IpList.objects.filter(idc=idc, network=network, status=1)
        ip_unactive = IpList.objects.filter(idc=idc, network=network, status=0)
        if not ip_active:
            ip_active, ip_unactive = ip_list_refresh(idc, network)

    return my_render('assets/ip_list_info.html', locals(), request)


@login_required
def ip_list_refresh(idc, network):
    nm = nmap.PortScanner()
    ip_active, ip_unactive = [], []
    ips = nm.scan(hosts=network, arguments='-v -sP -PE -n --min-hostgroup 1 --min-parallelism 1')['scan']
    for ip in ips:
        if ips[ip]['status']['state'] == 'up':
            ip_active.append(str(ip))
        else:
            ip_unactive.append(str(ip))
    sort_ip_list(ip_active)
    sort_ip_list(ip_unactive)
    IpList.objects.filter(idc=idc, network=network).delete()
    for ip in ip_active:
        IpList.objects.create(idc=idc, network=network, ip=ip, status=1)
    for ip in ip_unactive:
        IpList.objects.create(idc=idc, network=network, ip=ip, status=0)
    return ip_active, ip_unactive


@login_required
def MarkDown_edit(request, uuid):
    """ Markdown编缉器 """
    s = Project.objects.get(pk=uuid)
    data = Project_docForm()
    if request.method == 'POST':
        uf_post = Project_docForm(request.POST, instance=s)
        if uf_post.is_valid():
            zw = uf_post.save()
            zw.save()
            url = "%s&token=%s&options=%s" % (request.GET["next"], request.GET.get("token"), request.GET.get("options"))
            return HttpResponseRedirect(url)
    return render_to_response('markdown/index.html', locals(), context_instance=RequestContext(request))


@login_required
def MarkDown_select(request):
    """ Markdown编缉器 """
    data = Project.objects.all()

    return render_to_response('markdown/index.html', locals(), context_instance=RequestContext(request))


def MarkDown_content(request, uuid):
    s = Project.objects.get(pk=uuid)
    return HttpResponse(s.description)
