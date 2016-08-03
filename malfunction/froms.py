# coding:utf-8

from django import forms
from django.db import models

from models import Incident
from django import forms
from  DjangoUeditor.widgets import UEditorWidget
from  DjangoUeditor.forms import UEditorField, UEditorModelForm
from users.models import department_Mode, CustomUser
BOOL_STATUS = ((True, '是'), (False, '否'))

class inclident_from(UEditorModelForm):
    """
    """
    op = [("--------------", "--------------")]
    try:
        op_group = department_Mode.objects.get(desc_gid=1001)
        op_user = CustomUser.objects.filter(department=op_group)

        for i in op_user:
            op.append((i.first_name, i.first_name))
    except:
        pass

    project_status = forms.ChoiceField(widget=forms.RadioSelect, choices=BOOL_STATUS, required=True, initial=True,
                               label=u"是否通知项目负责人")
    projectuser = forms.CharField(max_length=32,
                widget=forms.Select(choices=op), label=u"业务负责人")
    class Meta:
        model = Incident
        fields = ['title', 'source', 'url', 'grade', 'mailcomment', 'starttime', 'scantime', 'stoptime', 'projectuser',
                  'comment', 'status', 'classical', 'project_principal', "project_status"
                  ]

class Editinclident_from(UEditorModelForm):
    """
    """
    class Meta:
        model = Incident
        fields = ['title', 'source', 'url', 'grade', 'mailcomment', 'starttime', 'scantime', 'stoptime', 'projectuser',
                  'comment', 'status', 'classical', 'project_principal'
                  ]

class zabbix_from(forms.ModelForm):
    """
    """

    class Meta:
        model = Incident
        fields = ['title', 'ip', 'grade', 'mailcomment', 'starttime']



class script_from(forms.ModelForm):
    """
    """

    class Meta:
        model = Incident
        fields = ['title', 'url', 'grade', 'mailcomment', 'starttime']


class smokeping_from(forms.ModelForm):
    """
    """

    class Meta:
        model = Incident
        fields = ['title', 'url', 'grade', 'mailcomment', 'starttime']



