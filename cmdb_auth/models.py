#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
#=============================================================================


from django.db import models
from users.models import CustomUser
from uuidfield import UUIDField
from assets.models import Project, Host

class auth_group(models.Model):
    """
    权限组
    """
    uuid = UUIDField(auto=True, primary_key=True)
    group_name = models.CharField(max_length=100, verbose_name=u'角色名称', unique=True)
    group_user = models.ManyToManyField(CustomUser, blank=True, verbose_name=u'所属用户')
    enable = models.BooleanField(default=True, verbose_name=u'是否启用')
    explanation = models.TextField(verbose_name=u'角色描述')
    date_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u"角色管理"
        verbose_name_plural = verbose_name


class user_auth_cmdb(models.Model):
    """
    cmdb权限
    所有字段全部以0，1来表示
    1表示有此权限，0表示无此权限
    所有数据全部外键关联user表，当用户删除时相应权限也随之删除
    """
    uuid = UUIDField(auto=True, primary_key=True)
    u"""
    资产管理
    """
    select_host = models.BooleanField(default=False, verbose_name=u"查看资产")
    edit_host = models.BooleanField(default=False, verbose_name=u"修改资产")
    update_host = models.BooleanField(default=False, verbose_name=u"更新资产")
    add_host = models.BooleanField(default=False, verbose_name=u"添加主机")
    bat_add_host = models.BooleanField(default=False, verbose_name=u"批量添加")
    delete_host = models.BooleanField(default=False, verbose_name=u"删除资产")
    add_line_auth = models.BooleanField(default=False, verbose_name=u"产品线管理")
    u"""
    发布权限
    """
    auth_project = models.BooleanField(default=False, verbose_name=u"自动化发布")
    auth_highstate = models.BooleanField(default=False, verbose_name=u"自动化部署")

    u"""
    用户管理
    """
    add_user = models.BooleanField(default=False, verbose_name=u'添加用户')
    edit_user = models.BooleanField(default=False, verbose_name=u'修改用户')
    edit_pass = models.BooleanField(default=False, verbose_name=u"修改密码")
    delete_user = models.BooleanField(default=False, verbose_name=u"删除用户")
    add_department = models.BooleanField(default=False, verbose_name=u"部门管理")

    u"""
    机房管理
    """

    select_idc = models.BooleanField(default=False, verbose_name=u"查看机房")
    add_idc = models.BooleanField(default=False, verbose_name=u"添加机房")
    edit_idc = models.BooleanField(default=False, verbose_name=u"修改机房")
    del_idc = models.BooleanField(default=False, verbose_name=u"删除机房")

    u"""
    系统管理
    """
    setup_system = models.BooleanField(default=False, verbose_name=u"安装系统")
    upload_system = models.BooleanField(default=False, verbose_name=u"主机上报")
    salt_keys = models.BooleanField(default=False, verbose_name=u"主机上报")

    u"""
    项目管理
    """
    project_auth = models.BooleanField(default=False, verbose_name=u"项目列表")
    add_project = models.BooleanField(default=False, verbose_name=u"添加项目")
    edit_project = models.BooleanField(default=False, verbose_name=u"修改项目")
    delete_project = models.BooleanField(default=False, verbose_name=u"删除项目")

    u"""
    日志管理
    """
    auth_log = models.BooleanField(default=False, verbose_name=u"salt执行记录")
    cmdb_log = models.BooleanField(default=False, verbose_name=u"资产操作记录")
    server_audit = models.BooleanField(default=False, verbose_name=u"服务器操作记录")


    group_name = models.ForeignKey(auth_group, verbose_name=u'所属角色', help_text=u"添加角色组权限")

    def __unicode__(self):
        return self.group_name
        # return u"权限管理"

    class Meta:
        verbose_name = u"权限管理"
        verbose_name_plural = verbose_name


class AuthSudo(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    groupname = models.CharField(max_length=64, verbose_name=u"组名", help_text=u"sudo组")
    shell = models.TextField(verbose_name=u'命令')
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        managed = True
        db_table = 'AuthSudo'
        verbose_name = u"sudo授权"
        verbose_name_plural = verbose_name


class AuthNode(models.Model):
    uuid = UUIDField(auto=True, primary_key=True)
    user_name = models.ForeignKey(CustomUser, max_length=20, verbose_name=u"名称", help_text=u"用户")
    node = models.ForeignKey(Host, null=True, blank=True, verbose_name=u'主机', on_delete=models.SET_NULL)
    auth = models.BooleanField(verbose_name=u'是否管理员', default=0)
    # project = models.CharField(verbose_name=u'项目名', max_length=128, blank=True, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.user_name

    class Meta:
        managed = True
        db_table = 'AuthNode'
        verbose_name = u"主机权限"
        verbose_name_plural = verbose_name
