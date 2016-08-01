#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# FileName: forms.py
# Desc: 2015-15/11/16:下午4:14
# Author: 苦咖啡
#        Email: voilet@qq.com
#     HomePage: http://blog.kukafei520.net
#      History: 
# =============================================================================

from django.shortcuts import render_to_response, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.template import RequestContext
from assets.models import Project, Host
from assets.models import project_swan, swan_pro, swan_port, gitCode
from django import forms
import ast
from django.contrib.auth.decorators import login_required


# class swan_form(forms.ModelForm):
#     """
#     """
#
#     choose = forms.ChoiceField(widget=forms.RadioSelect, choices=swan_pro, required=True, initial=0, label=u"发布类型")
#     node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")
#
#     def __init__(self, *args, **kwargs):
#         self.business = kwargs.pop('business', None)
#         super(swan_form, self).__init__(*args, **kwargs)
#         self.fields['ip'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)
#         # self.fields['ip'].choices = Host.objects.values_list("id", "eth1")
#
#     class Meta:
#         model = project_swan
#         fields = [
#             "swan_name",
#             "script",
#             "tgt",
#             "node",
#         ]


# class ProjectForm(forms.ModelForm):
#     node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")
#
#     def __init__(self, *args, **kwargs):
#         self.business = kwargs.pop('business', None)
#         super(ProjectForm, self).__init__(*args, **kwargs)
#         self.fields['node'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)
#
#     class Meta:
#         model = project_swan
#         fields = [
#             "swan_name",
#             "script",
#             "tgt",
#             'node'
#         ]


# class swan_all_form(forms.ModelForm):
#     """
#     sadf
#     """
#     check_port_status = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_port, required=True, initial=0,
#                                           label=u"是否检测端口")
#     choose = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_pro, required=True, initial=1, label=u"发布类型")
#     bat_push = forms.ChoiceField(widget=forms.RadioSelect(), choices=swan_port, required=True, initial=0, label=u"批量发布")
#
#     node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")
#
#     def __init__(self, *args, **kwargs):
#         self.business = kwargs.pop('business', None)
#         super(swan_all_form, self).__init__(*args, **kwargs)
#         self.fields['ip'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)
#
#     class Meta:
#         model = project_swan
#         fields = [
#             "choose",
#             "swan_name",
#             "config_name",
#             "salt_sls",
#             "bat_push",
#             "check_port_status",
#             "check_port",
#             "node",
#         ]


class GitCodeForm(forms.ModelForm):
    node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super(GitCodeForm, self).__init__(*args, **kwargs)
        self.fields['node'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)

    class Meta:
        model = project_swan
        fields = [
            "swan_name",
            "code_name",
            "git_code",
            "code_path",
            "git_code_user",
            # "git_tag",
            "tgt",
            "shell",
            "shell_status",
            "CheckUrl",
            'node'
        ]


class GitEditCodeForm(forms.ModelForm):
    node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super(GitEditCodeForm, self).__init__(*args, **kwargs)
        self.fields['node'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)

    class Meta:
        model = project_swan
        fields = [
            "swan_name",
            "code_name",
            "git_code",
            "code_path",
            "git_code_user",
            "tgt",
            "shell",
            "shell_status",
            "CheckUrl",
            'node'
        ]


class CodeForm(forms.ModelForm):
    class Meta:
        model = gitCode
        fields = [
            "codePath",
            "codeserver",
            "codeFqdn",
        ]


class ShellCodeForm(forms.ModelForm):
    node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super(ShellCodeForm, self).__init__(*args, **kwargs)
        self.fields['node'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)

    class Meta:
        model = project_swan
        fields = [
            "swan_name",
            "code_name",
            "shell",
            "tgt",
            "CheckUrl",
            'node'
        ]


class JavaCodeForm(forms.ModelForm):
    node = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=[], label=u"主机列表")

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super(JavaCodeForm, self).__init__(*args, **kwargs)
        self.fields['node'].choices = Host.objects.values_list("uuid", "eth1").filter(business=self.business)

    class Meta:
        model = project_swan
        fields = [
            "swan_name",
            "git_code",
            "code_name",
            "code_path",
            "git_code_user",
            "tgt",
            "tomcat_init",
            "cache",
            "shell",
            "shell_status",
            "CheckUrl",
            'node'
        ]
