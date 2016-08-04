#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#      History:
# =============================================================================

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
reload(sys)
sys.setdefaultencoding('utf-8')
gettext = lambda s: s

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!1%%l%20#**yj0i&hif_u5c^=$i&m3@1p!q*4w^3(bra3@xbnq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1"]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_pygments',
    'crispy_forms',
    'DjangoUeditor',
    'users',
    'assets',
    'accounts',
    'salt_ui',
    'pagination',
    'bootstrapform',
    'swan',
    'config',
    'audit',
    'bootstrap3',
    'cmdb_auth',
    'malfunction',
    'monitor',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 分页
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

    ('css', os.path.join(STATIC_ROOT, 'css').replace('\\', '/')),
    ('js', os.path.join(STATIC_ROOT, 'js').replace('\\', '/')),
    ('img', os.path.join(STATIC_ROOT, 'img').replace('\\', '/')),
    ('fonts', os.path.join(STATIC_ROOT, 'fonts').replace('\\', '/')),
    ('extra', os.path.join(STATIC_ROOT, 'extra').replace('\\', '/')),
    ('bootstrap', os.path.join(STATIC_ROOT, 'bootstrap').replace('\\', '/')),
    ('new', os.path.join(STATIC_ROOT, 'new').replace('\\', '/')),
    ('images', os.path.join(STATIC_ROOT, 'images').replace('\\', '/')),
    ('ztree', os.path.join(STATIC_ROOT, 'ztree').replace('\\', '/')),
    ('layer', os.path.join(STATIC_ROOT, 'layer').replace('\\', '/')),
    ('external', os.path.join(STATIC_ROOT, 'external').replace('\\', '/')),
    ('pdf', os.path.join(STATIC_ROOT, 'pdf').replace('\\', '/')),
    ('lib', os.path.join(STATIC_ROOT, 'lib').replace('\\', '/')),
    ('plugins', os.path.join(STATIC_ROOT, 'plugins').replace('\\', '/')),
    ('md', os.path.join(STATIC_ROOT, 'md').replace('\\', '/')),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# MEDIA_ROOT = os.path.join(BASE_DIR, 'upload/').replace('\\', '/')
# MEDIA_URL = '/media/'

upload_path = "%s/upload/" % BASE_DIR
MEDIA_ROOT = upload_path
MEDIA_URL = '/upload/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    'mysite.context_processors.user_session_expiry'
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

AUTH_USER_MODEL = 'users.CustomUser'

# UEDITOR_SETTINGS = {
#     "image_manager": {
#         "path": str(time.strftime('%Y/%m/%d/', time.localtime(time.time())))  # 图片管理器的位置,如果没有指定，默认跟图片路径上传一样
#     },
#     "scrawl_upload": {
#         "path": str(time.strftime('%Y/%m/%d/', time.localtime(time.time())))  # 涂鸦图片默认的上传路径
#     }
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # 'django.db.backends': {
        #     'handlers': ['console'],
        #     'level': 'DEBUG',
        # }
    }
}

EMAIL_HOST = 'mail.qq.com'
EMAIL_PORT = '25'
EMAIL_HOST_USER = 'devops'
EMAIL_HOST_PASSWORD = '123456'
EMAIL_USE_TLS = False
EMAIL_PUSH = True

# 发送邮件帐号
SendMail = "ops@xxx.com"


REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_DB = 0

django_path = os.getcwd()
localhost_path = "%s/mysite/%s" % (django_path, "localhost.py")
salt_config = "%s/mysite/%s" % (django_path, "prod.py")

# from mongoengine import *
# connect('config_center')
ops_mail = "songxs@fun.tv"

if os.path.isfile(localhost_path):
    from localhost import *
else:
    from prod import *

# BOOTSTRAP3 = {
#     'horizontal_label_class': 'col-md-3',
#     'horizontal_field_class': 'col-md-6',
# }
#
# BOOTSTRAP_COLUMN_COUNT = 10

# salt api info
salt_cdn_url = 'https://192.168.111.142/'
salt_center_url = 'https://192.168.111.101/'
salt_user = 'salt'
salt_passwd = '992a15aecbcf5727df775c45a35738cf'

# zabbix api info
zabbix_on = False
zabbix_url = 'http://192.168.111.47:8080/zabbix'
zabbix_user = 'admin'
zabbix_passwd = 'zabbix'


