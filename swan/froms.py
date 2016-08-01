# coding:utf-8

from django import forms
from django.db import models

from swan.models import Apply


class apply_from(forms.ModelForm):
    # FAVORITE_COLORS_CHOICES = Project.objects.values_list("id", "service_name")
    # business = forms.MultipleChoiceField(required=False,
    #     widget=forms.CheckboxSelectMultiple, choices=FAVORITE_COLORS_CHOICES)
    # core_num = models.SmallIntegerField(choices=Cores, blank=True, null=True, verbose_name=u'CPU核数')

    class Meta:
        model = Apply
        fields = ['owner', 'project_name', 'apply_name', 'qa_owner', 'op_owner', 'comment']
