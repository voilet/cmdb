# coding: utf-8
from assets.models import Project,ProjectUser

for one in Project.objects.filter():
    for user in one.service_user.all():
        a =ProjectUser.objects.get_or_create(user=user,myform=one)
