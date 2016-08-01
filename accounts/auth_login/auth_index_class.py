#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 
#      History:
#=============================================================================
import json
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from functools import wraps
from django.utils.decorators import available_attrs
# from mysite.settings import LOGIN_URL



def user_passes_test(test_func, login_url=None):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request):
                return view_func(request, *args, **kwargs)
            return HttpResponseRedirect(login_url)
        return _wrapped_view
    return decorator


#
# def auth_login_required(function=None, login_url=LOGIN_URL):
#     """
#     登陆验证
#     """
#     def is_authenticated(request):
#         if request.user.id:
#             return True
#         return False
#
#     actual_decorator = user_passes_test(is_authenticated, login_url=login_url)
#     if function:
#         return actual_decorator(function)
#     return actual_decorator
