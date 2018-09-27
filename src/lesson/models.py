#-*- coding:utf-8 -*-
from django.db import models
from django import forms
from django.forms import Form,fields,widgets,ValidationError
# Create your models here.
class Students(models.Model):
    name = models.CharField(verbose_name='学生姓名',max_length=30)
    class_name = models.CharField(verbose_name='班级',max_length=30)
    username = models.CharField(verbose_name='学号',max_length=30)
    password = models.CharField(verbose_name='密码',max_length=30)
    
    class Meta:
        verbose_name = '学生信息'
        verbose_name_plural = '学生信息'
        
    def __str__(self):
        return self.username
        

    
class lesson(models.Model):
    TYPE=(
        ('人文艺术类', '人文艺术类'),
        ('工程技术类','工程技术类'),
        ('经济管理类','经济管理类'),
        )
    TIME=(
        ('上午1-2节', '上午1-2节'),
        ('上午3-4节','上午3-4节'),
        ('下午5-6节','下午5-6节'),
        ('下午7-8节','下午7-8节'),
        ('晚上9-10节','晚上9-10节'),
        ('晚上11-12节','晚上11-12节')
        )
    lessonname = models.CharField(verbose_name='课程名称',max_length=30)
    teacher = models.CharField(verbose_name='任课老师',max_length=30)
    lessontype = models.CharField(verbose_name='课程类型',choices=TYPE,max_length=30)
    classroom = models.CharField(verbose_name='上课教室',max_length=30)
    time =models.CharField(verbose_name='上课时间',choices=TIME,max_length=30)
    week =models.CharField(verbose_name='起始-结束周',max_length=30)
    quantity = models.IntegerField(verbose_name='剩余数量')
    
    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = '课程信息'
        
    def __str__(self):
        return self.lessonname
        

class result(models.Model):
    rusername=models.CharField(verbose_name='学号',max_length=30)
    rname=models.CharField(verbose_name='学生姓名',max_length=30)
    rclass_name= models.CharField(verbose_name='班级',max_length=30)
    rlessonname= models.CharField(verbose_name='课程名称',max_length=30)
    rlessontype=models.CharField(verbose_name='课程类型',max_length=30)
    rteacher= models.CharField(verbose_name='任课老师',max_length=30)
    rclassroom= models.CharField(verbose_name='上课教室',max_length=30)
    rtime= models.CharField(verbose_name='上课时间',max_length=30)
    rweek= models.CharField(verbose_name='起始-结束周',max_length=30)
    
    class Meta:
        verbose_name = '选课结果'
        verbose_name_plural = '选课结果'
        
    def __str__(self):
        return self.rlessonname
    
    
    
    