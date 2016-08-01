#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: jiami.py
#         Desc: 2015-15/10/28:下午3:02
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import random
from random import Random
import os
import hashlib
# from hashlib import sha256, md5, new
from hmac import HMAC


class PyCrypt(object):
    """This class used to encrypt and decrypt password."""

    def __init__(self, key):
        self.key = key
        self.mode = AES.MODE_CBC

    def encrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        length = 64
        try:
            count = len(text)
        except TypeError:
            # raise ServerError('Encrypt password error, TYpe error.')
            pass
        add = (length - (count % length))
        text += ('\0' * add)
        ciphertext = cryptor.encrypt(text)
        return b2a_hex(ciphertext)

    def decrypt(self, text):
        cryptor = AES.new(self.key, self.mode, b'8122ca7d906ad5e1')
        try:
            plain_text = cryptor.decrypt(a2b_hex(text))
        except TypeError:
            # raise ServerError('Decrypt password error, TYpe error.')
            pass
        return plain_text.rstrip('\0')


def Pysalt():
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
    salt = ''.join(salt_list)
    return salt


def main():
    pc = PyCrypt('94c18fceef60b37d31e7a309635a5664') #初始化密钥
    s = Pysalt()
    e = pc.encrypt(s)  # 加密
    d = pc.decrypt(e)   # 解密
    print "加密:", e, len(e)
    print "解密:", d, len(d)
    return e

if __name__ == '__main__':
    main()