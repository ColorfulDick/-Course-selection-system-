#-*- coding:utf-8 -*-
from django.db import models
from django import forms
from django.forms import Form,fields,widgets,ValidationError
import os
import datetime
from captcha.fields import CaptchaField 
# Create your models here.
class Students(models.Model):
    name = models.CharField(verbose_name='学生姓名',max_length=30)
    class_name = models.CharField(verbose_name='班级',max_length=30)
    email = models.EmailField(max_length=50,verbose_name='邮箱',default='') 
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
    def get_photo(self, filename):
        return os.path.join('photo', '%s_%s_%s_%s' % (self.lessonname, self.teacher, self.classroom, os.path.splitext(filename)[1]))
    photo = models.ImageField(verbose_name='相关照片', upload_to=get_photo, blank=True, null=True)
    def get_movie(self, filename):
        return os.path.join('movie', '%s_%s_%s_%s' % (self.lessonname, self.teacher, self.classroom, os.path.splitext(filename)[1]))
    movie = models.FileField(max_length=200, upload_to=get_movie, default='videos/default.mp4', verbose_name='视频文件')
    
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

class EmailVerifyRecord(models.Model):   
    """邮箱激活码"""  
    code=models.CharField(max_length=20,verbose_name='验证码')   
    email=models.EmailField(max_length=50,verbose_name='邮箱')   
    send_type=models.CharField(verbose_name='验证码类型',choices=(('register','注册'),('forget','忘记密码')), max_length=20)   
    send_time=models.DateTimeField(verbose_name='发送时间',default=datetime.datetime.now())   
    class Meta:     
        verbose_name='邮箱验证码'    
        verbose_name_plural=verbose_name   
    def __str__(self):     
        return '{0}({1})'.format(self.code,self.email) 

class ForgetForm(forms.Form):   
    email=forms.EmailField(required=True)   
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'})   #reset.html中，用于验证新设的密码长度是否达标 
class ResetForm(forms.Form):   
    newpwd1=forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})   
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"}) 

    
    
    