#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName:
# Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
#   =============================================================================

from django.db import models
from users.models import CustomUser
from uuidfield import UUIDField
import datetime

BOOL_CHOICES = ((True, '使用中'), (False, '空闲'))

idc_type = (
    (0, u"CDN"),
    (1, u"核心")
)

idc_operator = (
    (0, u"电信"),
    (1, u"联通"),
    (2, u"移动"),
    (3, u"铁通"),
    (4, u"小带宽"),
)

SERVER_STATUS = (
    (0, u"未安装系统"),
    (1, u"已安装系统"),
    (2, u"正在安装系统"),
    (3, u"报废"),
)

ZABBIX_STATUS = (
    (0, u"添加失败"),
    (1, u"添加成功"),
    (2, u"添加失败,已存在"),
)

VM_STATUS = (
    (-1, u"apply machine"),
    (0, u"real machine"),
    (1, u"vitual machine"),
)

Server_System = [
    (i, i) for i in
    (
        u"Dell R210",
        u"Dell R410",
        u"Dell R420",
        u"Dell R510",
        u"Dell R620",
        u"Dell R710",
        u"Dell R720",
        u"Dell R720xd",
        u"Dell R730xd",
        u"HP",
        u"HP DL360p",
        u"HP DL380e",
        u"HP DL160",
        u"Lenovo",
        u"Lenovo WQ R510 G7",
        u"Lenovo ThinkServer RD330",
        u"Lenovo ThinkServer RD340",
        u"DIY",
        u"VIP",
        u"虚拟化",
        u"Other",
        u"MediaServer",
        u"网络设备",
    )
    ]

# System_os = [(i, i) for i in (u"CentOS", u"Centos 6.2")]
System_os = [(i, i) for i in (u"CentOS", u"Windows")]
Cores = [(i * 1, u"%s Cores" % (i * 1)) for i in range(1, 33)]
# system_arch = [(i, i) for i in (u"x86_64", u"x86_64")]
system_arch = [(u"x86_64", u"x86_64")]
System_usage = [(i, i) for i in (u"default", u"database")]
ENVIRONMENT = [(i, i) for i in (u"st", u"aws", u"prod", u"pub")]

# room_hours = [(i, i) for i in (u"3-2")]
room_hours = [(u"3-2", u"3-2")]

STATE_CHOICE = (
    (0, u"可申请"),
    (1, u"审批中"),
    (2, u"审批通过"),
)


class Line(models.Model):
    """
    产品线
    """
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=100, verbose_name=u"产品线")
    slug = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"别名")
    sort = models.IntegerField(max_length=100, blank=True, null=True, default=0, verbose_name=u"排序")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"产品线"
        verbose_name_plural = verbose_name


class Project(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    service_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'项目名')
    aliases_name = models.CharField(max_length=60, blank=True, null=True, verbose_name=u'别名，用于监控')
    project_contact = models.ForeignKey(CustomUser, related_name=u"main_business", verbose_name=u"主要负责人", )
    project_contact_backup = models.ForeignKey(CustomUser, related_name=u"backup_business", verbose_name=u"第二负责人")
    description = models.TextField(blank=True, null=True, verbose_name=u'业务说明')
    line = models.ForeignKey(Line, null=True, blank=True, related_name=u"business", verbose_name=u"产品线", db_index=False,
                             on_delete=models.SET_NULL)
    project_doc = models.TextField(blank=True, null=True, verbose_name=u'业务维护说明')
    project_user_group = models.TextField(blank=True, null=True, verbose_name=u'组成员', help_text=u"只有项目组成员才能申请发布")
    sort = models.IntegerField(max_length=100, blank=True, null=True, default=0, verbose_name=u"排序")
    def __unicode__(self):
        return self.service_name

    class Meta:
        verbose_name = u"业务"
        verbose_name_plural = verbose_name


class IDC(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=64, verbose_name=u'机房名称')
    bandwidth = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'机房带宽')
    phone = models.CharField(max_length=32, verbose_name=u'联系电话')
    linkman = models.CharField(max_length=32, null=True, verbose_name=u'联系人')
    address = models.CharField(max_length=128, blank=True, null=True, verbose_name=u"机房地址")
    network = models.TextField(blank=True, null=True, verbose_name=u"IP地址段")
    create_time = models.DateField(auto_now=True)
    operator = models.IntegerField(verbose_name=u"运营商", choices=idc_operator, max_length=32, blank=True, null=True)
    type = models.IntegerField(verbose_name=u"机房类型", choices=idc_type, max_length=32, blank=True, null=True)
    comment = models.TextField(blank=True, null=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"IDC机房"
        verbose_name_plural = verbose_name
        app_label = 'assets'


class Publishing_System(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    project_name = models.IntegerField(max_length=20, verbose_name=u"项目名称")
    push_url = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"发布按钮名称")

    def __unicode__(self):
        return self.project_name

    class Meta:
        verbose_name = u"发布系统"
        verbose_name_plural = verbose_name
        db_table = 'push_system'


class ProjectUser(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    project = models.ForeignKey(Project, db_index=False)
    user = models.ForeignKey(CustomUser, blank=True, null=True, on_delete=models.SET_NULL, related_name=u"all_business")
    data_created = models.DateTimeField(auto_now_add=True)
    env = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"项目环境")

    def __unicode__(self):
        return self.myform.service_name

    class Meta:
        verbose_name = u"业务管理人员"
        verbose_name_plural = verbose_name


class Service(models.Model):
    """
    基础服务，如nginx, haproxy, php....
    """
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=30, unique=True, verbose_name=u"服务名称",
                            help_text=u'注意，所有服务操作全部期于linux服务操作，如: "service iptables restart"')
    port = models.IntegerField(null=True, blank=True, verbose_name=u"端口")
    remark = models.TextField(null=True, blank=True, verbose_name=u"备注")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u"服务"
        verbose_name_plural = verbose_name


class Host(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    node_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=u"主机名")
    idc = models.ForeignKey(IDC, blank=True, null=True, verbose_name=u'机房', on_delete=models.SET_NULL)
    eth1 = models.IPAddressField(blank=True, null=True, verbose_name=u'网卡1')
    eth2 = models.IPAddressField(blank=True, null=True, verbose_name=u'网卡2')
    mac = models.CharField(max_length=20, blank=True, null=True, verbose_name=u"MAC")
    internal_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'远控卡')
    brand = models.CharField(max_length=64, choices=Server_System, blank=True, null=True, verbose_name=u'硬件厂商')
    cpu = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'CPU')
    hard_disk = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'硬盘')
    memory = models.CharField(max_length=128, blank=True, null=True, verbose_name=u'内存')
    system = models.CharField(verbose_name=u"系统类型", max_length=32, choices=System_os, default="CentOS", blank=True,
                              null=True, )
    system_cpuarch = models.CharField(max_length=32, blank=True, null=True, choices=system_arch, verbose_name=u"系统版本")
    system_version = models.CharField(max_length=8, blank=True, null=True, verbose_name=u"版本号")
    create_time = models.DateTimeField(auto_now_add=True)
    guarantee_date = models.DateField(blank=True, null=True, verbose_name=u'保修时间')
    cabinet = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'机柜号')
    server_cabinet_id = models.IntegerField(blank=True, null=True, verbose_name=u'机器位置')
    number = models.CharField(max_length=32, blank=True, null=True, verbose_name=u'资产编号')
    editor = models.TextField(blank=True, null=True, verbose_name=u'备注')
    business = models.ManyToManyField(Project, blank=True, null=True, verbose_name=u'所属业务')
    u"""
    0   未安装系统
    1   已安装系统
    2   正在安装中
    3   报废
    """
    status = models.IntegerField(verbose_name=u"机器状态", choices=SERVER_STATUS, default=0, blank=True)
    vm = models.ForeignKey("self", blank=True, null=True, verbose_name=u"虚拟机父主机")
    type = models.IntegerField(verbose_name=u'主机类型', default=1, blank=True, max_length=2)
    Services_Code = models.CharField(max_length=16, blank=True, null=True, verbose_name=u"快速服务编码")
    env = models.CharField(max_length=32, blank=True, null=True, verbose_name=u"环境", choices=ENVIRONMENT)
    room_number = models.CharField(verbose_name=u"房间号", max_length=32, choices=room_hours, blank=True, null=True)
    server_sn = models.CharField(verbose_name=u"SN编号", max_length=32, blank=True, null=True)
    switch_port = models.CharField(verbose_name=u"端口号", max_length=12, blank=True, null=True)
    service = models.ManyToManyField(Service, verbose_name=u'运行服务', blank=True, null=True)
    idle = models.BooleanField(verbose_name=u'状态', default=1, choices=BOOL_CHOICES)

    def __unicode__(self):
        return self.node_name

    class Meta:
        verbose_name = u"服务器"
        verbose_name_plural = verbose_name


class HostRecord(models.Model):
    """ 主机修改记录model """
    uuid = UUIDField(auto=True, primary_key=True)
    host = models.ForeignKey(Host)
    user = models.CharField(max_length=30, null=True)
    time = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)


swan_pro = (
    (0, u"普通"),
    (1, u"基础服务"),
    (2, u"git仓库发布"),
    (3, u"java发布"),
    (4, u"shell发布"),
)

swan_port = (
    (0, u"否"),
    (1, u"是"),
)

argall_select = (
    (0, u"all"),
    (1, u"Single"),
)


class gitCode(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    codePath = models.CharField(verbose_name=u'本地存放路径', max_length=64, help_text=u'存放路径如/data/code')
    codeserver = models.CharField(verbose_name=u'发布代码服务器', max_length=64, help_text=u'线上发布代码仓库或aws发布仓库')
    codeFqdn = models.CharField(verbose_name=u'salt主机名', max_length=64)

    def __unicode__(self):
        return self.codeFqdn

    class Meta:
        managed = True
        db_table = 'gitCode'
        verbose_name = u"git仓库"
        verbose_name_plural = verbose_name


class project_swan(models.Model):
    """
    发布系统字段
    """
    uuid = UUIDField(auto=True, primary_key=True)
    swan_name = models.CharField(max_length=100, verbose_name=u"发布名称", help_text=u"发布时同一项目有多个按布按钮，此处设置为发布选项名称")
    code_name = models.CharField(max_length=100, default="", verbose_name=u"仓库名称",
                                 help_text=u"发布时同一项目有多个按布按钮，此处设置为发布选项名称")
    project_name = models.ForeignKey(Project, verbose_name=u"项目名", help_text=u"一个项目可以添加多个发布功能", null=True,
                                     blank=True, on_delete=models.SET_NULL)
    choose = models.CharField(choices=swan_pro, max_length=10, verbose_name=u"选择")
    check_port_status = models.BooleanField(verbose_name=u"是否检测端口", default=0)
    check_port = models.CharField(max_length=30, verbose_name=u'检测业务端口', null=True, blank=True,
                                  help_text=u'业务启动端口检测,多个端口用逗号分割')
    bat_push = models.IntegerField(verbose_name=u'批量推送', default=0, help_text=u'是否批量推送或单台进行发布')
    tgt = models.TextField(null=True, blank=True, verbose_name=u"选择发布分支或参数", help_text=u'可以有多个分支或参数，多个参数换行填写即可')
    argall_str = models.CharField(max_length=20, null=True, blank=True, choices=argall_select, verbose_name=u"发布参数")
    node = models.ManyToManyField(Host, null=True, blank=True, verbose_name=u'主机')
    push_user = models.ManyToManyField(CustomUser, null=True, blank=True, verbose_name=u"发布权限")

    tomcat_init = models.CharField(verbose_name=u'tomcat起动脚本', max_length=128, blank=True, null=True,
                                   help_text=u"默认为/etc/init.d/tomcat如多个项目可能有多个名称,请根据名称进行填写")
    cache = models.TextField(null=True, blank=True, verbose_name=u"缓存目录", help_text=u'tomcat启动前需要清除的目录')

    git_code = models.ForeignKey(gitCode, verbose_name=u'发布仓库', default="", blank=True, null=True,
                                 help_text=u"如未填写,则默认以服务器目录git仓库为准,接取代码会直接pull不会有其它操作")

    git_code_user = models.CharField(verbose_name=u'所属用户', max_length=12, blank=True, null=True,
                                     help_text=u'代码权限所属用户,比如php代码为nginx用户组',
                                     )
    code_path = models.CharField(verbose_name=u'本地代码存放目录', max_length=128, blank=True, null=True,
                                 help_text=u'当中转仓库更新完代码,需要通知目标服务器pull代码',
                                 )
    git_user = models.CharField(verbose_name=u'仓库帐号', max_length=12, blank=True, null=True,
                                help_text=u'如未填写则使使用默认帐号密码,创建后不可修改')
    git_pass = models.CharField(verbose_name=u'仓库密码', max_length=64, blank=True, null=True,
                                help_text=u'如未填写则使使用默认帐号密码,创建后不可修改')
    shell = models.CharField(verbose_name=u'shell脚本', max_length=128, blank=True, null=True,
                             help_text=u'发布后执行脚本')
    shell_status = models.BooleanField(verbose_name=u'发布前/后执行脚本', help_text=u'指定发布前或发布后执行脚本', default=False)
    CheckUrl = models.URLField(verbose_name=u'检测URL', blank=True, null=True,
                               help_text=u'在发布时,如业务不能单台发布则需要填写此URL,发布时检测业务是否正常在加入调度')
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.swan_name

    class Meta:
        managed = True
        db_table = 'project_swan'
        verbose_name = u"项目发布"
        verbose_name_plural = verbose_name


class ZabbixRecord(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    name = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    status = models.IntegerField(null=True, blank=True, choices=ZABBIX_STATUS)
    info = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.name


class IpList(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    idc = models.ForeignKey(IDC, verbose_name=u"IDC")
    network = models.CharField(max_length=32, null=True)
    ip = models.CharField(max_length=16, null=True)
    status = models.IntegerField(null=True)

    def __unicode__(self):
        return self.ip
