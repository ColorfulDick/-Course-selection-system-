# -*- coding:utf-8 -*-
import time
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Students,lesson,result
from django.contrib.auth.hashers import make_password,check_password 
from django import forms    #导入表单
from django.contrib.auth.models import User   #导入django自带的user表
from django.db.models import Count
 
# Django的form的作用：
# 1、生成html标签
# 2、用来做用户提交的验证
# Form的验证思路
# 前端：form表单
# 后台：创建form类，当请求到来时，先匹配，匹配出正确和错误信息。
def index(request):
    if request.method == 'GET':     # 获取所有学生信息    
        ticket = request.COOKIES.get('ticket')     
        if not ticket:       
            return HttpResponseRedirect('/login/')     
        if Students.objects.filter(u_ticket=ticket).exists():       
            stuinfos = Students.objects.all()       
            return render(request, 'index.html', {'stuinfos': stuinfos})     
        else:       
            return HttpResponseRedirect('/login/') 

 
def regist(request):
    if request.method == 'GET':
        return render(request, 'regist1.html')
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        name = request.POST['name']
        class_name = request.POST['class_name']
        if Students.objects.filter(username=username).exists():
            return HttpResponse('您已经注册过了')
        else:
            password = make_password(password)#对密码进行加密
            Students.objects.create(username=username, password=password,name=name,class_name=class_name)
            return HttpResponse('注册成功')
    
def login(request):
    if request.method == 'GET':     
        return render(request, 'login.html')
         
    if request.method == 'POST':     
        # 如果登录成功，绑定参数到cookie中，set_cookie     
        username = request.POST['username']     
        password = request.POST['password']     
        # 查询用户是否在数据库中    
        if Students.objects.filter(username=username).exists():       
            user = Students.objects.get(username=username)       
            if check_password(password, user.password):# ticket = 'agdoajbfjad'         
                response = HttpResponseRedirect('/selectlesson/')         #max_age 存活时间(秒)         
                response.set_cookie('ticket', username, max_age=10000)   # 存在服务端         
                return response       
            else:         # return HttpResponse('用户密码错误')         
                return render(request, 'login.html', {'password': '用户密码错误'})     
        else:       # return HttpResponse('用户不存在')       
            return render(request, 'login.html', {'username': '用户不存在'}) 

  
def logout(request):
    def logout(request):   
        if request.method == 'GET':     # response = HttpResponse()     
            response = HttpResponseRedirect('/login/')     
            response.delete_cookie('ticket')     
            return response 


def selectlesson(request):
    username=request.COOKIES.get('ticket')
    stu=Students.objects.get(username=username)
    name = stu.name
    class_name = stu.class_name
    lessonlist = lesson.objects.all()  #将User表中的所有对象赋值给users这个变量，它是一个列表
    if request.method == 'GET':
        return render(request, 'selectlesson.html', {'lessonlists': lessonlist,'name':name})#生成一个lessonlist、name变量，这个变量可以给templates中的html文件使用
    elif  request.method == 'POST':
            check_box_list = request.POST.getlist("check_box_list")
            for les in check_box_list:
                trans=lesson.objects.get(lessonname=les)
                lessontype=trans.lessontype
                teacher=trans.teacher
                classroom=trans.classroom
                time=trans.time
                week=trans.week
                quantity=trans.quantity
                num=result.objects.filter(rusername=username).count()
                print(num)
                if num>1:
                    return HttpResponse('您已经选了两门课，不能再选了')
                else:
                    if quantity>0:
                        qua=lesson.objects.get(lessonname=les)
                        qua.quantity=quantity-1
                        qua.save()#学生选了这门课，课程数量-1
                        result.objects.create(rusername=username,rname=name,rclass_name=class_name,rlessonname=les,rlessontype=lessontype,rteacher=teacher,rclassroom=classroom,rtime=time,rweek=week)
                        return HttpResponse('恭喜您，选课成功')
                    else:
                        return HttpResponse('这门课已经被选完了，再看看吧')
                

def managelesson(request):
    username = request.COOKIES.get('ticket')
    managelist=result.objects.filter(rusername=username)
    stu = Students.objects.get(username=username)
    name = stu.name
    if request.method=='GET':
        return render(request, 'managelesson.html', {'managelists': managelist,'name':name})
    elif request.method=='POST':
        check_box_list = request.POST.getlist("check_box_list")
        for les in check_box_list:
            qua=lesson.objects.get(lessonname=les)
            quantity=qua.quantity
            qua.quantity=quantity+1
            qua.save()#学生退选，课程剩余数量+1
            result.objects.filter(rlessonname=les).delete()
        return  HttpResponse('该删的都删了')
