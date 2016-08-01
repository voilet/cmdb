#!/usr/bin/env python
#-*- coding: utf-8 -*-
#=============================================================================
#     FileName:
#         Desc:
#       Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      Version: 0.0.1
#   LastChange: 2013-02-20 14:52:11
#      History:
#=============================================================================

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from assets.value_class.froms import Engine_RoomForm
from django.http import HttpResponseRedirect
from assets.models import IDC, Project
# from accounts.auth_login.auth_index_class import auth_login_required
from django.contrib.auth.decorators import login_required
from cmdb_auth.no_auth import check_auth

@login_required
@csrf_protect
def add_room(request):
    """
    添加机房
    """
    status = check_auth(request, "add_idc")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    server_type = Project.objects.all()
    if request.method == 'POST':    
        uf = Engine_RoomForm(request.POST)   
        if uf.is_valid(): 
            uf.save()
            return HttpResponseRedirect("/assets/server/room/list/")
    else:
        uf = Engine_RoomForm()
    return render_to_response('assets/server_room_add.html', locals(), context_instance=RequestContext(request))

#机房列表
@login_required
@csrf_protect
def room_list(request):
    status = check_auth(request, "select_idc")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    room_list = IDC.objects.all()
    server_type = Project.objects.all()
    return render_to_response('assets/server_room_list.html', locals(), context_instance=RequestContext(request))

#修改机房
@login_required
@csrf_protect
def room_edit(request, id):
    status = check_auth(request, "edit_idc")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    room = IDC.objects.get(id=id)
    if request.method == 'POST':    
        uf = Engine_RoomForm(request.POST, instance=room)   
        if uf.is_valid(): 
            uf.save()
            return HttpResponseRedirect("/assets/server/room/list/")
    uf = Engine_RoomForm(instance=room)

    return render_to_response('assets/server_room_add.html', locals(), context_instance=RequestContext(request))

#删除机房
@login_required
@csrf_protect
def room_delete(request,id):
    status = check_auth(request, "del_idc")
    if not status:
        return render_to_response('default/error_auth.html', locals(), context_instance=RequestContext(request))

    room = IDC.objects.get(id=id)
    #TODO give a alert list page to show the host in this idc
    # hosts = room.
    room.delete()
    return HttpResponseRedirect("/assets/server/room/list/")