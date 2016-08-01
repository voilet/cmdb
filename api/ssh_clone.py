#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: ssh_clone
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/1/18 下午2:31
     History:   
"""

import sys

reload(sys)
sys.setdefaultencoding('utf8')
import pwd
import os
import re
import time
import datetime
import textwrap
import getpass
import readline
import django
import paramiko
import errno
import struct, fcntl, signal, socket, select
from io import open as copen
import uuid
import logging

LOG_DIR = "/tmp/aaa.log"

login_user = getpass.getuser()
try:
    remote_ip = os.environ.get('SSH_CLIENT').split()[0]
except (IndexError, AttributeError):
    remote_ip = os.popen("who -m | awk '{ print $NF }'").read().strip('()\n')

try:
    import termios
    import tty
except ImportError:
    print '\033[1;31m仅支持类Unix系统 Only unix like supported.\033[0m'
    time.sleep(3)
    sys.exit()


def color_print(msg, color='red', exits=False):
    """
    Print colorful string.
    颜色打印字符或者退出
    """
    color_msg = {'blue': '\033[1;36m%s\033[0m',
                 'green': '\033[1;32m%s\033[0m',
                 'yellow': '\033[1;33m%s\033[0m',
                 'red': '\033[1;31m%s\033[0m',
                 'title': '\033[30;42m%s\033[0m',
                 'info': '\033[32m%s\033[0m'}
    msg = color_msg.get(color, 'red') % msg
    print msg
    if exits:
        time.sleep(2)
        sys.exit()
    return msg



def write_log(f, msg):
    msg = re.sub(r'[\r\n]', '\r\n', msg)
    f.write(msg)
    f.flush()


def chown(path, user, group=''):
    if not group:
        group = user
    try:
        uid = pwd.getpwnam(user).pw_uid
        gid = pwd.getpwnam(group).pw_gid
        os.chown(path, uid, gid)
    except KeyError:
        pass



def mkdir(dir_name, username='', mode=0755):
    """
    insure the dir exist and mode ok
    目录存在，如果不存在就建立，并且权限正确
    """
    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)
        os.chmod(dir_name, mode)
    if username:
        chown(dir_name, username)

class Tty(object):
    """
    A virtual tty class
    一个虚拟终端类，实现连接ssh和记录日志，基类
    """

    def __init__(self, user, asset, role, login_type='ssh'):
        self.username = user
        self.asset_name = "192.168.8.80"
        self.ip = None
        self.port = 22
        self.ssh = None
        self.channel = None
        self.asset = asset
        self.user = user
        self.role = role
        self.remote_ip = ''
        self.login_type = login_type
        self.vim_flag = False
        self.ps1_pattern = re.compile('\[.*@.*\][\$#]')
        self.vim_data = ''

    @staticmethod
    def is_output(strings):
        newline_char = ['\n', '\r', '\r\n']
        for char in newline_char:
            if char in strings:
                return True
        return False

    @staticmethod
    def remove_obstruct_char(cmd_str):
        '''删除一些干扰的特殊符号'''
        control_char = re.compile(r'\x07 | \x1b\[1P | \r ', re.X)
        cmd_str = control_char.sub('', cmd_str.strip())
        patch_char = re.compile('\x08\x1b\[C')  # 删除方向左右一起的按键
        while patch_char.search(cmd_str):
            cmd_str = patch_char.sub('', cmd_str.rstrip())
        return cmd_str

    @staticmethod
    def deal_backspace(match_str, result_command, pattern_str, backspace_num):
        '''
        处理删除确认键
        '''
        if backspace_num > 0:
            if backspace_num > len(result_command):
                result_command += pattern_str
                result_command = result_command[0:-backspace_num]
            else:
                result_command = result_command[0:-backspace_num]
                result_command += pattern_str
        del_len = len(match_str) - 3
        if del_len > 0:
            result_command = result_command[0:-del_len]
        return result_command, len(match_str)

    @staticmethod
    def deal_replace_char(match_str, result_command, backspace_num):
        '''
        处理替换命令
        '''
        str_lists = re.findall(r'(?<=\x1b\[1@)\w', match_str)
        tmp_str = ''.join(str_lists)
        result_command_list = list(result_command)
        if len(tmp_str) > 1:
            result_command_list[-backspace_num:-(backspace_num - len(tmp_str))] = tmp_str
        elif len(tmp_str) > 0:
            if result_command_list[-backspace_num] == ' ':
                result_command_list.insert(-backspace_num, tmp_str)
            else:
                result_command_list[-backspace_num] = tmp_str
        result_command = ''.join(result_command_list)
        return result_command, len(match_str)

    def remove_control_char(self, result_command):
        """
        处理日志特殊字符
        """
        control_char = re.compile(r"""
                \x1b[ #%()*+\-.\/]. |
                \r |                                               #匹配 回车符(CR)
                (?:\x1b\[|\x9b) [ -?]* [@-~] |                     #匹配 控制顺序描述符(CSI)... Cmd
                (?:\x1b\]|\x9d) .*? (?:\x1b\\|[\a\x9c]) | \x07 |   #匹配 操作系统指令(OSC)...终止符或振铃符(ST|BEL)
                (?:\x1b[P^_]|[\x90\x9e\x9f]) .*? (?:\x1b\\|\x9c) | #匹配 设备控制串或私讯或应用程序命令(DCS|PM|APC)...终止符(ST)
                \x1b.                                              #匹配 转义过后的字符
                [\x80-\x9f] | (?:\x1b\]0.*) | \[.*@.*\][\$#] | (.*mysql>.*)      #匹配 所有控制字符
                """, re.X)
        result_command = control_char.sub('', result_command.strip())

        if not self.vim_flag:
            if result_command.startswith('vi') or result_command.startswith('fg'):
                self.vim_flag = True
            return result_command.decode('utf8', "ignore")
        else:
            return ''

    def deal_command(self, str_r):
        """
            处理命令中特殊字符
        """
        str_r = self.remove_obstruct_char(str_r)

        result_command = ''  # 最后的结果
        backspace_num = 0  # 光标移动的个数
        reach_backspace_flag = False  # 没有检测到光标键则为true
        pattern_str = ''
        while str_r:
            tmp = re.match(r'\s*\w+\s*', str_r)
            if tmp:
                str_r = str_r[len(str(tmp.group(0))):]
                if reach_backspace_flag:
                    pattern_str += str(tmp.group(0))
                    continue
                else:
                    result_command += str(tmp.group(0))
                    continue

            tmp = re.match(r'\x1b\[K[\x08]*', str_r)
            if tmp:
                result_command, del_len = self.deal_backspace(str(tmp.group(0)), result_command, pattern_str,
                                                              backspace_num)
                reach_backspace_flag = False
                backspace_num = 0
                pattern_str = ''
                str_r = str_r[del_len:]
                continue

            tmp = re.match(r'\x08+', str_r)
            if tmp:
                str_r = str_r[len(str(tmp.group(0))):]
                if len(str_r) != 0:
                    if reach_backspace_flag:
                        result_command = result_command[0:-backspace_num] + pattern_str
                        pattern_str = ''
                    else:
                        reach_backspace_flag = True
                    backspace_num = len(str(tmp.group(0)))
                    continue
                else:
                    break

            tmp = re.match(r'(\x1b\[1@\w)+', str_r)  # 处理替换的命令
            if tmp:
                result_command, del_len = self.deal_replace_char(str(tmp.group(0)), result_command, backspace_num)
                str_r = str_r[del_len:]
                backspace_num = 0
                continue

            if reach_backspace_flag:
                pattern_str += str_r[0]
            else:
                result_command += str_r[0]
            str_r = str_r[1:]

        if backspace_num > 0:
            result_command = result_command[0:-backspace_num] + pattern_str

        result_command = self.remove_control_char(result_command)
        return result_command

    def get_log(self):
        """
        Logging user command and output.
        记录用户的日志
        """
        tty_log_dir = os.path.join(LOG_DIR, 'tty')
        date_today = datetime.datetime.now()
        date_start = date_today.strftime('%Y%m%d')
        time_start = date_today.strftime('%H%M%S')
        today_connect_log_dir = os.path.join(tty_log_dir, date_start)
        log_file_path = os.path.join(today_connect_log_dir, '%s_%s_%s' % (self.username, self.asset_name, time_start))

        try:
            mkdir(os.path.dirname(today_connect_log_dir), mode=0777)
            mkdir(today_connect_log_dir, mode=0777)
        except OSError:
            logging.debug('创建目录 %s 失败，请修改%s目录权限' % (today_connect_log_dir, tty_log_dir))
            print('创建目录 %s 失败，请修改%s目录权限' % (today_connect_log_dir, tty_log_dir))

        try:
            log_file_f = open(log_file_path + '.log', 'a')
            log_time_f = open(log_file_path + '.time', 'a')
        except IOError:
            logging.debug('创建tty日志文件失败, 请修改目录%s权限' % today_connect_log_dir)
            print('创建tty日志文件失败, 请修改目录%s权限' % today_connect_log_dir)

        if self.login_type == 'ssh':  # 如果是ssh连接过来，记录connect.py的pid，web terminal记录为日志的id
            pid = os.getpid()
            self.remote_ip = remote_ip  # 获取远端IP
        else:
            pid = 0

        # log = Log(user=self.username, host=self.asset_name, remote_ip=self.remote_ip, login_type=self.login_type,
        #           log_path=log_file_path, start_time=date_today, pid=pid)
        # log.save()
        # if self.login_type == 'web':
        #     log.pid = log.id  # 设置log id为websocket的id, 然后kill时干掉websocket
        #     log.save()
        #
        # log_file_f.write('Start at %s\r\n' % datetime.datetime.now())
        # log_file_f.close()

        print log_file_f, log_time_f, True
        return log_file_f, log_time_f, True
        # return log_file_f, log_time_f, "aaa"


    def get_connection(self):
        """
        获取连接成功后的ssh
        """
        # connect_info = self.get_connect_info()

        # 发起ssh连接请求 Make a ssh connection
        ssh = paramiko.SSHClient()
        # ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:

            key = paramiko.RSAKey.from_private_key_file("/Users/voilet/.ssh/id_rsa")
            ssh.connect("192.168.8.80", port=self.port, username="root", pkey=key
                        )

        except paramiko.ssh_exception.AuthenticationException, paramiko.ssh_exception.SSHException:
            print('认证失败 Authentication Error.')
        except socket.error:
            print('端口可能不对 Connect SSH Socket Port Error, Please Correct it.')
        else:
            self.ssh = ssh
            return ssh


class SshTty(Tty):
    """
    A virtual tty class
    一个虚拟终端类，实现连接ssh和记录日志
    """

    @staticmethod
    def get_win_size():
        """
        This function use to get the size of the windows!
        获得terminal窗口大小
        """
        if 'TIOCGWINSZ' in dir(termios):
            TIOCGWINSZ = termios.TIOCGWINSZ
        else:
            TIOCGWINSZ = 1074295912L
        s = struct.pack('HHHH', 0, 0, 0, 0)
        x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
        return struct.unpack('HHHH', x)[0:2]

    def set_win_size(self, sig, data):
        """
        This function use to set the window size of the terminal!
        设置terminal窗口大小
        """
        try:
            win_size = self.get_win_size()
            self.channel.resize_pty(height=win_size[0], width=win_size[1])
        except Exception:
            pass

    def posix_shell(self):
        """
        Use paramiko channel connect server interactive.
        使用paramiko模块的channel，连接后端，进入交互式
        """
        log_file_f, log_time_f, log = self.get_log()
        old_tty = termios.tcgetattr(sys.stdin)
        pre_timestamp = time.time()
        data = ''
        input_mode = False
        try:
            tty.setraw(sys.stdin.fileno())
            tty.setcbreak(sys.stdin.fileno())
            self.channel.settimeout(0.0)

            while True:
                try:
                    r, w, e = select.select([self.channel, sys.stdin], [], [])
                    flag = fcntl.fcntl(sys.stdin, fcntl.F_GETFL, 0)
                    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flag | os.O_NONBLOCK)
                except Exception:
                    pass

                if self.channel in r:
                    try:
                        x = self.channel.recv(10240)
                        if len(x) == 0:
                            break
                        if self.vim_flag:
                            self.vim_data += x
                        index = 0
                        len_x = len(x)
                        while index < len_x:
                            try:
                                n = os.write(sys.stdout.fileno(), x[index:])
                                sys.stdout.flush()
                                index += n
                            except OSError as msg:
                                if msg.errno == errno.EAGAIN:
                                    continue
                        # sys.stdout.write(x)
                        # sys.stdout.flush()
                        now_timestamp = time.time()
                        log_time_f.write('%s %s\n' % (round(now_timestamp - pre_timestamp, 4), len(x)))
                        log_time_f.flush()
                        log_file_f.write(x)
                        log_file_f.flush()
                        pre_timestamp = now_timestamp
                        log_file_f.flush()

                        if input_mode and not self.is_output(x):
                            data += x

                    except socket.timeout:
                        pass

                if sys.stdin in r:
                    try:
                        x = os.read(sys.stdin.fileno(), 4096)
                    except OSError:
                        pass
                    input_mode = True
                    if str(x) in ['\r', '\n', '\r\n']:
                        if self.vim_flag:
                            match = self.ps1_pattern.search(self.vim_data)
                            if match:
                                self.vim_flag = False
                                data = self.deal_command(data)[0:200]
                                # if len(data) > 0:
                                #     TtyLog(log=log, datetime=datetime.datetime.now(), cmd=data).save()
                        else:
                            data = self.deal_command(data)[0:200]
                            if len(data) > 0:
                                pass
                                # TtyLog(log=log, datetime=datetime.datetime.now(), cmd=data).save()
                        data = ''
                        self.vim_data = ''
                        input_mode = False

                    if len(x) == 0:
                        break
                    self.channel.send(x)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_tty)
            log_file_f.write('End time is %s' % datetime.datetime.now())
            log_file_f.close()
            log_time_f.close()
            # log.is_finished = True
            # log.end_time = datetime.datetime.now()
            # log.save()
        # except:
        #     pass

    def connect(self):
        """
        Connect server.
        连接服务器
        """
        # 发起ssh连接请求 Make a ssh connection
        ssh = self.get_connection()

        transport = ssh.get_transport()
        transport.set_keepalive(30)
        transport.use_compression(True)

        # 获取连接的隧道并设置窗口大小 Make a channel and set windows size
        global channel
        win_size = self.get_win_size()
        # self.channel = channel = ssh.invoke_shell(height=win_size[0], width=win_size[1], term='xterm')
        self.channel = channel = transport.open_session()
        channel.get_pty(term='xterm', height=win_size[0], width=win_size[1])
        channel.invoke_shell()
        try:
            signal.signal(signal.SIGWINCH, self.set_win_size)
        except:
            pass

        self.posix_shell()

        # Shutdown channel socket
        channel.close()
        ssh.close()


class Nav(object):
    """
    导航提示类
    """

    def __init__(self, user):
        self.user = user
        self.search_result = {}
        self.user_perm = {}

    @staticmethod
    def print_nav():
        """
        Print prompt
        打印提示导航
        """
        msg = """\n\033[1;32m###    欢迎使用跳板机系统   ### \033[0m
        1) 输入 \033[32mID\033[0m 直接登录.
        2) 输入 \033[32m/\033[0m + \033[32mIP, 主机名 or 备注 \033[0m搜索.
        3) 输入 \033[32mP/p\033[0m 显示您有权限的主机.
        4) 输入 \033[32mG/g\033[0m 显示您有权限的主机组.
        5) 输入 \033[32mG/g\033[0m\033[0m + \033[32m组ID\033[0m 显示该组下主机.
        6) 输入 \033[32mE/e\033[0m 批量执行命令.
        7) 输入 \033[32mU/u\033[0m 批量上传文件.
        8) 输入 \033[32mD/d\033[0m 批量下载文件.
        9) 输入 \033[32mH/h\033[0m 帮助.
        0) 输入 \033[32mQ/q\033[0m 退出.
        """
        print textwrap.dedent(msg)

    def search(self, str_r=''):
        # gid_pattern = re.compile(r'^g\d+$')
        # 获取用户授权的所有主机信息
        # if not self.user_perm:
        #     self.user_perm = get_group_user_perm(self.user)
        # user_asset_all = self.user_perm.get('asset').keys()
        # # 搜索结果保存
        # user_asset_search = []
        # if str_r:
        #     # 资产组组id匹配
        #     if gid_pattern.match(str_r):
        #         gid = int(str_r.lstrip('g'))
        #         # 获取资产组包含的资产
        #         user_asset_search = get_object(AssetGroup, id=gid).asset_set.all()
        #     else:
        #         # 匹配 ip, hostname, 备注
        #         for asset in user_asset_all:
        #             if str_r in asset.ip or str_r in str(asset.hostname) or str_r in str(asset.comment):
        #                 user_asset_search.append(asset)
        # else:
        #     # 如果没有输入就展现所有
        #     user_asset_search = user_asset_all
        #
        # self.search_result = dict(zip(range(len(user_asset_search)), user_asset_search))
        # color_print('[%-3s] %-12s %-15s  %-5s  %-10s  %s' % ('ID', '主机名', 'IP', '端口', '系统用户', '备注'), 'title')
        # for index, asset in self.search_result.items():
        #     # 获取该资产信息
        #     asset_info = get_asset_info(asset)
        #     # 获取该资产包含的角色
        #     role = [str(role.name) for role in self.user_perm.get('asset').get(asset).get('role')]
        #     print '[%-3s] %-15s %-15s  %-5s  %-10s  %s' % (index, asset.hostname, asset.ip, asset_info.get('port'),
        #                                                    role, asset.comment)
        print "\n"
        print

    def exec_cmd(self):
        """
        批量执行命令
        """
        while True:
            if not self.user_perm:
                self.user_perm = get_group_user_perm(self.user)

            roles = self.user_perm.get('role').keys()
            if len(roles) > 1:  # 授权角色数大于1
                color_print('[%-2s] %-15s' % ('ID', '系统用户'), 'info')
                role_check = dict(zip(range(len(roles)), roles))

                for i, r in role_check.items():
                    print '[%-2s] %-15s' % (i, r.name)
                print
                print "请输入运行命令所关联系统用户的ID, q退出"

                try:
                    role_id = raw_input("\033[1;32mRole>:\033[0m ").strip()
                    if role_id == 'q':
                        break
                except (IndexError, ValueError):
                    color_print('错误输入')
                else:
                    role = role_check[int(role_id)]
            elif len(roles) == 1:  # 授权角色数为1
                role = roles[0]
            assets = list(self.user_perm.get('role', {}).get(role).get('asset'))  # 获取该用户，角色授权主机
            print "授权包含该系统用户的所有主机"
            for asset in assets:
                print ' %s' % asset.hostname
            print
            print "请输入主机名或ansile支持的pattern, 多个主机:分隔, q退出"
            pattern = raw_input("\033[1;32mPattern>:\033[0m ").strip()
            if pattern == 'q':
                break
            else:
                res = gen_resource({'user': self.user, 'asset': assets, 'role': role}, perm=self.user_perm)
                runner = MyRunner(res)
                asset_name_str = ''
                print "匹配主机:"
                for inv in runner.inventory.get_hosts(pattern=pattern):
                    print ' %s' % inv.name
                    asset_name_str += '%s ' % inv.name
                print

                while True:
                    print "请输入执行的命令， 按q退出"
                    command = raw_input("\033[1;32mCmds>:\033[0m ").strip()
                    if command == 'q':
                        break
                    runner.run('shell', command, pattern=pattern)
                    # ExecLog(host=asset_name_str, user=self.user.username, cmd=command, remote_ip=remote_ip,
                    #         result=runner.results).save()
                    for k, v in runner.results.items():
                        if k == 'ok':
                            for host, output in v.items():
                                color_print("%s => %s" % (host, 'Ok'), 'green')
                                print output
                                print
                        else:
                            for host, output in v.items():
                                color_print("%s => %s" % (host, k), 'red')
                                color_print(output, 'red')
                                print
                    print "~o~ Task finished ~o~"
                    print


def main():
    """
    he he
    主程序
    """
    if not login_user:  # 判断用户是否存在
        color_print('没有该用户，或许你是以root运行的 No that user.', exits=True)

    gid_pattern = re.compile(r'^g\d+$')
    nav = Nav(login_user)
    nav.print_nav()

    try:
        while True:
            try:
                option = raw_input("\033[1;32mOpt or ID>:\033[0m ").strip()
            except EOFError:
                nav.print_nav()
                continue
            except KeyboardInterrupt:
                sys.exit(0)
            if option in ['P', 'p', '\n', '']:
                nav.search()
                continue
            if option.startswith('/') or gid_pattern.match(option):
                nav.search(option.lstrip('/'))
            elif option in ['H', 'h']:
                nav.print_nav()
            elif option in ['Q', 'q', 'exit']:
                sys.exit()
            else:
                ssh_tty = SshTty(login_user, "192.168.8.80", "/Users/voilet/.ssh/id_rsa")
                ssh_tty.connect()
                continue
    except IndexError, e:
        color_print(e)
        time.sleep(5)
        pass


if __name__ == '__main__':
    main()
