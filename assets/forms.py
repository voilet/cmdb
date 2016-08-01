# coding:utf-8
from django import forms
from assets.models import Host, IDC, Service, Project




class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ["node_name", "idc", "room_number", "eth1", "eth2", "mac", "internal_ip", "room_number", "cabinet",
                  "server_cabinet_id", "number", "business", "service", "env", "status",
                  "cpu", "hard_disk", "memory", "system", "system_cpuarch", "vm", "Services_Code",
                  "brand", "guarantee_date", "server_sn", "idle", "editor"]


class IdcForm(forms.ModelForm):
    class Meta:
        model = IDC
        fields = ['name', "bandwidth", "operator", 'type', 'linkman', 'phone', 'network', 'address', 'comment']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'port', 'remark']


class Project_docForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["description"]
