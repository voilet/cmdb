#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    FileName: cmdb_excel.py
        Desc:
      Author: 苦咖啡
       Email: voilet@qq.com
    HomePage: http://blog.kukafei520.net
     Version: 0.0.1
  LastChange: 16/2/22 下午4:47
     History:   
"""
import xlrd
from django.http import HttpResponse
from assets.models import Host, IDC
import json
from users.models import cmdb_uuid


def xls_select(request):
    """ http监控列表 """
    data = xlrd.open_workbook('/Users/voilet/Documents/cmdb.xls')
    table = data.sheet_by_name(u'cmdb')
    nrows = table.nrows
    s = 0
    for i in range(1, nrows):
        ip = str(table.cell(i, 9).value).strip()
        # if Host.objects.filter(eth1=ip).count() == 0:
        # Host.objects.get(eth1=ip)
        try:
            rst = Host.objects.get(eth1=ip)
            if table.cell(i, 6).value and table.cell(i, 7).value:
                rst.cabinet = str(table.cell(i, 6).value)
                rst.server_cabinet_id = int(table.cell(i, 7).value)
                rst.system_cpuarch = u"x86_64"

            else:
                print ip
            rst.brand = u"%s" % str(table.cell(i, 4).value)
            rst.save()
        except Host.DoesNotExist:
            # print str(ip).strip()
            s += 1
            node_conf = str(table.cell(i, 5).value).split("/")
            ctc = IDC.objects.get(name="亦庄电信")
            cnc = IDC.objects.get(name="北京联通")
            ip_search = str(ip).split(".")
            cnc1 = "%s.%s.%s" % (ip_search[0], ip_search[1], ip_search[2])
            # rst = Host(cabinet=str(table.cell(i, 6).value), server_cabinet_id=int(table.cell(i, 7).value))
            # print len(node_conf)
            if len(node_conf) == 3:
                print ip
                # print ip_search, type(ip_search)

                rst = Host(eth1=ip,
                           node_name=ip,
                           internal_ip=ip,
                           memory=node_conf[1],
                           hard_disk=node_conf[-1],
                           cpu=node_conf[0],
                           system="CentOS",
                           cabinet=table.cell(i, 6).value,
                           number=table.cell(i, 1).value,
                           server_sn=table.cell(i, 2).value,
                           Services_Code=table.cell(i, 3).value,
                           server_cabinet_id=table.cell(i, 7).value,
                           editor=table.cell(i, 12).value,
                           brand=str(table.cell(i, 4).value),
                           status=1,
                           )

            else:
                print ip
                print "*" * 100
                rst = Host(eth1=ip,
                           node_name=ip,
                           internal_ip=ip,
                           system="CentOS",
                           cabinet=table.cell(i, 6).value,
                           number=table.cell(i, 1).value,
                           server_sn=table.cell(i, 2).value,
                           Services_Code=table.cell(i, 3).value,
                           editor=table.cell(i, 12).value,
                           brand=str(table.cell(i, 4).value),
                           status=1,
                           )
            if str(ip_search[2]) == "219" or cnc1 == "114.66.198" or cnc1 == "123.125.20":
                rst.idc = cnc
            else:
                rst.idc = ctc
            if str(table.cell(i, 4).value) == u"虚拟机":
                rst.type = 0
            if table.cell(i, 6).value and table.cell(i, 7).value:
                rst.cabinet = str(table.cell(i, 6).value)
                rst.server_cabinet_id = int(table.cell(i, 7).value)
                rst.system_cpuarch = u"x86_64"
            rst.save()

            # print rst
            # rst.save()
    print s

    return HttpResponse(json.dumps({"retCode": 200, "retMsg": "ok"}, ensure_ascii=False, indent=4))


def xls_cdn(request):
    """ http监控列表 """
    data = xlrd.open_workbook('/Users/voilet/Documents/cdn.xls')
    cdn_data = data.sheet_by_name(u'cdn')
    cdn_result = cdn_data.nrows
    for s in range(1, cdn_result):
        ip = str(cdn_data.cell(s, 9).value).strip()
        sn = str(cdn_data.cell(s, 4).value).strip()
        idc = str(cdn_data.cell(s, 14).value).strip()
        internal_ip = str(cdn_data.cell(s, 10).value).strip()
        number = str(cdn_data.cell(s, 3).value).strip()
        server_sn = str(cdn_data.cell(s, 18).value).strip()
        Services_Code = str(cdn_data.cell(s, 19).value).strip()
        cpu = str(cdn_data.cell(s, 6).value).strip()
        memory = str(cdn_data.cell(s, 7).value).strip()
        hard_disk = str(cdn_data.cell(s, 8).value).strip()
        cabinet = str(cdn_data.cell(s, 13).value).strip()

        if len(ip) > 0:
            print ip, idc, internal_ip, number, server_sn, Services_Code, cpu, memory, hard_disk, cabinet
            try:
                idc_data = IDC.objects.get(name=idc)
            except:
                uuid = str(cmdb_uuid()).replace("-", "")
                idc_data = IDC(name=idc, pk=uuid, phone=11111111111, linkman=u"曾阳", address=idc, )
                idc_data.save()
            try:
                rst = Host.objects.get(eth1=ip)
                rst.idc=idc_data
            except Host.DoesNotExist:
                rst = Host(eth1=ip,
                           idc=idc_data,
                           node_name=ip,
                           internal_ip=internal_ip,
                           system="CentOS",
                           status=1,
                           )
            # rst.save()

    # print error_list
    # print len(error_list)
    # s = open("/Users/voilet/test.txt", "r")
    # rst = s.readlines()
    # # print rst
    # result = {}
    # for i in rst:
    #     i = str(i).split()
    #     if len(i) == 3:
    #         ip = i[-1]
    #         idc = i[0]
    #         sn = i[1]
    #         result[sn] = {"idc": idc, "ip": ip}
    #
    #         print sn, idc, ip, "ok"
    #     else:
    #         print i, "error"
    # s.close()
    # s = 0
    # for i in range(1, nrows):
    #     ip = str(table.cell(i, 9).value).strip()
    #     # if Host.objects.filter(eth1=ip).count() == 0:
    #     # Host.objects.get(eth1=ip)
    #     try:
    #         Host.objects.get(eth1=ip)
    #     except Host.DoesNotExist:
    #         # print str(ip).strip()
    #         s += 1
    #         node_conf = str(table.cell(i, 5).value).split("/")
    #         ctc = IDC.objects.get(name="亦庄电信")
    #         cnc = IDC.objects.get(name="北京联通")
    #         ip_search = str(ip).split(".")[2]
    #         if len(node_conf) != 1:
    #
    #             # print ip_search, type(ip_search)
    #
    #             rst = Host(eth1=ip,
    #                        node_name=ip,
    #                        internal_ip=ip,
    #                        memory=node_conf[1],
    #                        hard_disk=node_conf[-1],
    #                        cpu=node_conf[0],
    #                        system="CentOS",
    #                        cabinet=table.cell(i, 6).value,
    #                        number=table.cell(i, 1).value,
    #                        server_sn=table.cell(i, 2).value,
    #                        Services_Code=table.cell(i, 3).value,
    #                        server_cabinet_id=table.cell(i, 7).value,
    #                        editor=table.cell(i, 12).value,
    #                        # idc=cnc,
    #                        status=1,
    #                        )
    #
    #         else:
    #             print ip
    #             rst = Host(eth1=ip,
    #                        node_name=ip,
    #                        internal_ip=ip,
    #                        system="CentOS",
    #                        cabinet=table.cell(i, 6).value,
    #                        number=table.cell(i, 1).value,
    #                        server_sn=table.cell(i, 2).value,
    #                        Services_Code=table.cell(i, 3).value,
    #                        editor=table.cell(i, 12).value,
    #                        status=1,
    #                        )
    #             if str(ip_search) == "219":
    #                 rst.idc = cnc
    #             else:
    #                 rst.idc = ctc
    #             rst.save()
    #
    #             # print rst
    #             # rst.save()
    # print s

    return HttpResponse(json.dumps({"retCode": 200, "retMsg": "ok"}, ensure_ascii=False, indent=4))
