# coding:utf-8
import urllib
import urllib2
import json
import ssl


from IPy import IP
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class SaltApi(object):
    __token_id = ''

    def __init__(self, url, username, password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password

    def post_request(self, obj, prefix='/'):
        url = self.__url + prefix
        headers = {'X-Auth-Token': self.__token_id}
        req = urllib2.Request(url, obj, headers)
        context = ssl._create_unverified_context()
        opener = urllib2.urlopen(req, context=context)
        content = json.loads(opener.read())
        return content

    def token_id(self):
        params = {'eauth': 'pam', 'username': self.__user, 'password': self.__password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        content = self.post_request(obj, prefix='/login')
        try:
            self.__token_id = content['return'][0]['token']
        except KeyError:
            raise KeyError

    def remote_exec(self, tgt, fun, arg):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun, 'arg': arg}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.post_request(obj)
        ret = content['return'][0][tgt]
        return ret

    def remote_noarg_exec(self, tgt, fun):
        params = {'client': 'local', 'tgt': tgt, 'fun': fun}
        obj = urllib.urlencode(params)
        self.token_id()
        content = self.post_request(obj)
        print content['return'][0]
        ret = content['return'][0].get(tgt)
        if ret:
            return ret
        else:
            return []


def page_list_return(total, current=1):
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page+1)


def pages(posts, r):
    """分页公用函数"""
    contact_list = posts
    p = paginator = Paginator(contact_list, 50)
    try:
        current_page = int(r.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(p.page_range), current_page)

    try:
        contacts = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0
    if current_page <= (len(p.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    return contact_list, p, contacts, page_range, current_page, show_first, show_end


def sort_ip_list(ip_list):
    """ ip地址排序 """
    ip_list.sort(key=lambda s: map(int, s.split('.')))
    return ip_list


def get_mask_ip(mask):
    """ 得到一个网段所有ip """
    ips = IP(mask)
    ip_list = []
    for ip in ips:
        ip_list.append(str(ip))
    ip_list = ip_list[1:]
    return ip_list

