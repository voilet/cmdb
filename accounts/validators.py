#!/usr/bin/python
# -*-coding:utf-8-*-

import re
from django.core.validators import RegexValidator

username_re = re.compile(r'^([\w]{9}|[a-zA-Z]{1}[\w]+?)$')
username = RegexValidator(username_re, u'学生:您的学号,管理员:4-12位,由字母数字下划线组成,首字母为字母', 'invalid')


password_re = re.compile(r'([^a-z0-9A-Z])+')
# password_re = re.compile(r'^[\w]+?$')
password = RegexValidator(password_re, u'密码由字母数字特殊符号组成的字符串，最少为6位', 'invalid')


def checklen(pwd):
    return len(pwd) >= 8


def checkContainUpper(pwd):
    pattern = re.compile('[A-Z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkContainNum(pwd):
    pattern = re.compile('[0-9]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkContainLower(pwd):
    pattern = re.compile('[a-z]+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkSymbol(pwd):
    pattern = re.compile('([^a-z0-9A-Z])+')
    match = pattern.findall(pwd)
    if match:
        return True
    else:
        return False


def checkPassword(pwd):
    lenOK = checklen(pwd)
    # upperOK = checkContainUpper(pwd)
    lowerOK = checkContainLower(pwd)
    numOK = checkContainNum(pwd)
    symbolOK = checkSymbol(pwd)
    return (lenOK  and lowerOK and numOK and symbolOK)
    # return (lenOK and upperOK and lowerOK and numOK and symbolOK)

#
def Checkpasswd(passwd):
    if checkPassword(passwd):
        print passwd
        return True
    else:
        return False
#
