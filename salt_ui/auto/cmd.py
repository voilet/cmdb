# coding=UTF-8
from django.shortcuts import render_to_response, render, HttpResponse
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.shortcuts import get_object_or_404
from salt_ui.api.salt_token_id import *
from salt_ui.api.salt_https_api import salt_api_jobs
from mysite.settings import salt_api_pass, salt_api_user, salt_api_url, pxe_url_api, websocket_url
from mysite.settings import auth_content, app_key, app_name, auth_url, auth_key

from salt_ui.views.api_log_class import salt_log
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
from utils.user_help import *
from utils.redis_help import *

from accounts.utils import jmmail

import yaml
from config.security import hacker_select


@login_required
def button_cmd_run(request):
    d = {
        'disk_blkid': 'disk.blkid',
        'disk_inodeusage': 'disk.inodeusage',
        'disk_percent': 'disk.percent',
        'disk_usage': 'disk.usage',

        'nginx_configtest': 'nginx.configtest',
        'nginx_status': 'nginx.status',
        'nginx_version': 'nginx.version',

        'network_active_tcp': 'network.active_tcp',
        'network_arp': 'network.arp',
        'network_connect': 'network.connect',  # host, port, timeout, proto
        'network_dig': 'network.dig',
        'network_netstat': 'network.netstat',

        'ps_top': 'ps.top',
        'ps_get_users': 'ps.get_users',
        'ps_cpu_times': ['ps.cpu_times', [True, ]],  # arg per_cpu=True
        'ps_pgrep': 'ps.pgrep',  # pattern

        'cmd_tail': 'cmd.run',
        'list_log': ['cmd.run', ['ls -LR /home/web_log', ]],
    }
    cmd = request.GET.get('cmd', None)
    fun = d.get(cmd, None)
    node_list = request.GET.getlist("node_name")
    if not fun or not node_list:
        return HttpResponse('缺少主机或者缺少命令')

    token_api_id = token_id()
    arg = []
    s = 'button_cmd_run'

    project = request.GET.get("project")
    # if "admin" not in request.user.department or "jumeiops" not in request.user.department:
    # print node_list, project
    # hack_status = hacker_select(node_list, project, request.user.username)
    # if not hack_status:
    #     return render_to_response('saltstack/salt_cmd_security.html',
    #                               locals(), context_instance=RequestContext(request))

    if isinstance(fun, list):
        fun, arg = fun
    if cmd == 'ps_pgrep':
        pattern = request.GET.get('pattern', '')
        arg.append(pattern)
    elif cmd == 'network_connect':
        host = request.GET.get('host', '')
        port = request.GET.get('port', None)
        arg += [host, port]
    elif cmd == 'network_dig':
        host = request.GET.get('host', '')
        arg.append(host)
        s = None
    elif cmd == 'cmd_tail':
        path = request.GET.get('path', None)
        if not path:
            return HttpResponse('缺少文件路径')
        num = request.GET.get('num', 100)
        if not num:
            num = 100
        cmd_tail = "tail -n %s %s" % (num, path)
        arg.append(cmd_tail)
        s = None
    elif cmd.startswith('nginx_') or cmd == 'list_log':
        s = None

    data = {'fun': fun, 'tgt': node_list, 'expr_form': 'list',
            'ret': 'redis', "client": "local"}
    if arg:
        data['arg'] = arg
    print data
    list_all = salt_api_token(data,
                              salt_api_url, {'X-Auth-Token': token_api_id})
    list_all = list_all.CmdRun()
    print list_all
    result = list_all["return"][0]
    # jid = result['jid']
    # # 日志入库
    # salt_log(request.user.username, node_list, int(jid), "执行命令", len(node_list), cmd, jid)

    return render(request, 'autoinstall/cmd_run.html', locals())


# @login_required
@csrf_protect
def cmd_run(request):
    if request.method == 'POST':
        data = request.POST.copy()
        node_list = data.getlist("node_name")  # minions
        cmd_type = request.GET.get("args", False)
        cmd = data.get("salt_cmd", None)  #
        token_api_id = token_id()
        project = data.get("project")
        if cmd_type == "cmd":
            # 如果使用危险命令则返回无权限
            der_cmd = cmd.replace(";", " ").split()
            if len(cmd) == 0:
                salt_cmd = cmd
                return render_to_response('autoinstall/cmd_run_status.html',
                                          locals(), context_instance=RequestContext(request))
            for drop_shell in der_cmd:
                drop = drop_shell.split(";")
                drop_data = "<h3>操作人: %s<br>主机列表：%s<br><br>命令: %s</h3><br>" % (request.user.username, node_list, cmd)

                if drop[0] in auth_content:
                    return render_to_response('autoinstall/cmd_run.html', locals(),
                                              context_instance=RequestContext(request))

            list_all = salt_api_token({'fun': 'cmd.run', 'tgt': node_list,
                                       'arg': cmd},
                                      salt_api_url, {'X-Auth-Token': token_api_id})
            list_all = list_all.CmdRun()
            result = list_all["return"][0]
            fqdn_sum = len(node_list)
            return render_to_response('autoinstall/cmd_run.html', locals(), context_instance=RequestContext(request))

        # 如果选择类型是grains
        elif cmd_type == "grains":
            if len(cmd) == 0:
                salt_cmd = cmd
                return render_to_response('autoinstall/cmd_run_status.html',
                                          locals(), context_instance=RequestContext(request))
            list_all = salt_api_token({'fun': 'grains.item', 'tgt': node_list,
                                       'arg': cmd,},
                                      salt_api_url, {'X-Auth-Token': token_api_id})
            list_all = list_all.run()
            result = list_all["return"][0]
            jid = result['jid']
            # 日志入库
            salt_log(request.user.username, node_list, int(jid), "推送配置", len(node_list), cmd, jid)

            return render_to_response('autoinstall/cmd_run.html',
                                      locals(), context_instance=RequestContext(request))
        else:
            return render_to_response('autoinstall/cmd_run_status.html',
                                      locals(), context_instance=RequestContext(request))


def handle_redis(request):
    # jid = request.GET.get("jid")
    # content = get_redis_result(jid)
    return render_to_response('autoinstall/redis_content.html', locals(), context_instance=RequestContext(request))


def highstate_redis(request):
    opts = {'extension_modules': '/var/cache/salt/master/extmods',
            'color': False,
            'state_verbose': True,
            }

    jid = request.GET.get("jid")
    content = get_redis_result(jid)
    content_data = {}
    from salt.output import display_output
    for i in content:
        s = {i: content[i]}
        data = display_output(s, "highstate", opts=opts)
        content_data[i] = data
    return render_to_response('autoinstall/redis_highstate.html', locals(), context_instance=RequestContext(request))
