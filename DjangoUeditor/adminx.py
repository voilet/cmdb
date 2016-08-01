#coding:utf-8
#__author__ = 'sai'
#DjangoUeditor Xadmin plugin

import xadmin
from django.db.models import TextField
from xadmin.views import BaseAdminPlugin, ModelFormAdminView, DetailAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget
from django.conf import settings

class XadminUEditorWidget(UEditorWidget):
    def __init__(self,**kwargs):
        self.ueditor_settings=kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)

class UeditorPlugin(BaseAdminPlugin):

    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                return {'widget': XadminUEditorWidget(**db_field.formfield().widget.attrs)}
            if isinstance(db_field, TextField):
                return {'widget': XadminUEditorWidget}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.config.js")
        js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.all.min.js")
        nodes.append(js)

xadmin.site.register_plugin(UeditorPlugin, DetailAdminView)
xadmin.site.register_plugin(UeditorPlugin, ModelFormAdminView)
