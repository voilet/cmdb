#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
import uuid
from django.contrib.auth.models import BaseUserManager
import random, time
import hashlib

manager_demo = [(i, i) for i in (u"经理", u"主管", u"项目责任人", u"管理员", u"BOOS")]
Department = [(u"ops", u"plat", u'dev')]
auth_id = [(u"普通用户", u"普通用户"), (u"管理员", u"管理员")]
auth_gid = [(1001, u"运维部"), (1002, u"架构"), (1003, u"研发"), (1004, u"测试")]


def cmdb_uuid():
    """
    :return:
    """
    salt_key = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*()_'
    symbol = '!@$%^&*()_'
    salt_list = []
    for i in range(60):
        salt_list.append(random.choice(salt_key))
    for i in range(4):
        salt_list.append(random.choice(symbol))
    salt = "%s%s%s" % (''.join(salt_list), time.time(), uuid.uuid4())
    uuid_data = str(uuid.uuid3(uuid.NAMESPACE_DNS, salt))
    return uuid_data


class DepartmentGroup(models.Model):
    department_groups_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'组名')
    description = models.TextField(verbose_name=u"介绍", blank=True, null=True, )

    def __unicode__(self):
        return self.department_groups_name

    class Meta:
        verbose_name = u"部门组"
        verbose_name_plural = verbose_name


class department_Mode(models.Model):
    department_name = models.CharField(max_length=64, blank=True, null=True, verbose_name=u'部门名称')
    description = models.TextField(verbose_name=u"介绍", blank=True, null=True, )
    desc_gid = models.IntegerField(verbose_name=u"部门组", choices=auth_gid, blank=True, null=True, )

    def __unicode__(self):
        return self.department_name

    class Meta:
        verbose_name = u"部门"
        verbose_name_plural = verbose_name


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          date_joined=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_(u'邮箱'), max_length=254, unique=True)
    username = models.CharField(_(u'用户名'), max_length=30, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)

    department = models.ForeignKey(department_Mode, blank=True, null=True, verbose_name=u"部门", related_name="users")
    mobile = models.CharField(_(u'手机'), max_length=30, blank=False,
                              validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                    _('Enter a valid mobile number.'),
                                                                    'invalid')])
    session_key = models.CharField(max_length=60, blank=True, null=True, verbose_name=u"session_key")
    user_key = models.TextField(blank=True, null=True, verbose_name=u"用户登录key")
    menu_status = models.BooleanField(default=False, verbose_name=u'用户菜单状态')
    user_active = models.BooleanField(verbose_name=u'设置密码状态', default=0)
    uuid = models.CharField(max_length=64, unique=True)

    # uuid = models.CharField(default=str(uuid.uuid3(uuid.NAMESPACE_DNS, hashlib.md5(str(time.time()) + str("".join(
    #         [random.choice("1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@$%^&*()_") for i in
    #          range(60)])) + str(uuid.uuid4())).hexdigest())), max_length=64)

    # Admin
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class server_auth(models.Model):
    server_ip = models.IPAddressField(blank=True, null=True, verbose_name=u'服务器')
    user_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'用户名')
    first_name = models.CharField(max_length=20, blank=True, null=True, verbose_name=u'姓名')
    auth_weights = models.BooleanField(default=0, verbose_name=u'权限')
    datetime = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.server_ip

    class Meta:
        verbose_name = u"日志记录"
        verbose_name_plural = verbose_name


if __name__ == '__main__':
    print cmdb_uuid()
