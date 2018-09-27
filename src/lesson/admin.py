# -*- coding:utf-8 -*-
#from django.contrib import admin
from lesson.models import *
import xadmin
# Register your models here.
class StudentsAdmin(object):
    list_display = ('username','name', 'class_name',)
    search_fields = ('username','name','class_name',)
class lessonAdmin(object):
    list_display = ('lessonname','lessontype','teacher',)
    search_fields = ('lessonname','lessontype','teacher',)
class resultAdmin(object):
    list_display = ('rusername','rname', 'rclass_name','rlessonname','rteacher')
    search_fields = ('rusername','rname','rclass_name','rlessonname','rteacher')

xadmin.site.register(Students, StudentsAdmin)
xadmin.site.register(lesson, lessonAdmin)
xadmin.site.register(result,resultAdmin)
xadmin.AdminSite.site_header ='选课系统后台'
xadmin.AdminSite.site_title = '选修课课管理系统'