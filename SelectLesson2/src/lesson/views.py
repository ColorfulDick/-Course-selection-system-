# -*- coding:utf-8 -*-
import time
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .models import Students,lesson,result,ForgetForm,ResetForm,EmailVerifyRecord
from django.contrib.auth.hashers import make_password,check_password 
from django.views import View
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont
import random
from django.core.mail import send_mail 
from SelectLesson2.settings import EMAIL_FROM
from io import BytesIO
from random import Random 
# Django的form的作用：
# 1、生成html标签
# 2、用来做用户提交的验证
# Form的验证思路
# 前端：form表单
# 后台：创建form类，当请求到来时，先匹配，匹配出正确和错误信息。
def index(request):
    if request.method == 'GET':     # 获取所有学生信息    
        username = request.COOKIES.get('ticket')     
        if not username:       
            return HttpResponseRedirect('/login/')     
        if Students.objects.filter(username=username).exists():       
            stuinfos = Students.objects.all()       
            return render(request, 'index.html', {'stuinfos': stuinfos})     
        else:       
            return HttpResponseRedirect('/login/') 

 
def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    if request.method == 'POST': 
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        name = request.POST['name']
        class_name = request.POST['class_name']
        email = request.POST['email']
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():  
            if Students.objects.filter(username=username).exists():
                return HttpResponse('您已经注册过了,请直接登录')
            else:
                password = make_password(password)#对密码进行加密
                Students.objects.create(username=username, password=password,name=name,class_name=class_name,email=email)
                return HttpResponse('注册成功')
        else:
            messages.success(request,"验证码错误，请重新填写")
            return render(request,'regist.html',{'valid_code':'验证码错误，请重新填写'})
        
def login(request):
    if request.method == 'GET':     
        return render(request, 'login.html')
         
    if request.method == 'POST':     
        # 如果登录成功，绑定参数到cookie中，set_cookie     
        username = request.POST['username']     
        password = request.POST['password']
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper():     
            # 查询用户是否在数据库中    
            if Students.objects.filter(username=username).exists():       
                user = Students.objects.get(username=username)       
                if check_password(password, user.password):# 验证密码         
                    response = HttpResponseRedirect('/selectlesson/')         #max_age 存活时间(秒)         
                    response.set_cookie('ticket', username, max_age=10000)   # 存在服务端         
                    return response       
                else:
                    messages.success(request,"用户密码错误，请重新填写")         # return HttpResponse('用户密码错误')         
                    return render(request, 'login.html', {'password': '用户密码错误'})     
            else:
                messages.success(request,"用户不存在")       # return HttpResponse('用户不存在')       
                return render(request, 'login.html', {'username': '用户不存在'}) 
        else:
            messages.success(request,"验证码错误，请重新填写")
            return render(request,'login.html',{'valid_code':'验证码错误，请重新填写'})

  
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
 
def video(request):
     return render(request, 'video.html',)               

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

def get_valid_img(request):  #调用Pillow模块绘制验证码，其实用captcha也可以的
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("/static/font/ygyxsziti2.0.ttf", 40)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 220  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

def random_str(random_length=8):   
    str=''   
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  
    length=len(chars)-1  
    random=Random()   
    for i in range(random_length):     
        str+=chars[random.randint(0,length)]   
    return str  
def send_register_email(email,send_type):   
    email_record=EmailVerifyRecord()         #用于生成随机验证码和对应的邮箱并存入数据库中，将验证码以链接形式发送至邮箱，点击进行激活
    code=random_str(16)   
    email_record.code=code   
    email_record.email=email   
    email_record.send_type=send_type   
    email_record.save()     
    email_title=''   
    email_body=''     
    if send_type=='forget':     
        email_title = '选课系统密码重置链接'    
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)       
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])     
        if send_status:       
            pass 

class ForgetPwdView(View):  
    '''忘记密码'''    
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'forget.html',{'forget_form':forget_form})
    def post(self,request):     
        forget_form = ForgetForm(request.POST)     
        if forget_form.is_valid():       
            email=request.POST.get('email','')       
            send_register_email(email,'forget')       
            return render(request,'success_send.html')     
        else:       
            return render(request,'forget.html',{'forget_form':forget_form})
             
class ResetView(View):   
    '''重置密码'''  
    def get(self,request,active_code):     
        record=EmailVerifyRecord.objects.filter(code=active_code)     
        print(record)     
        if record:       
            for i in record:         
                email=i.email         
                is_register=Students.objects.filter(email=email)         
                if is_register:           
                    return render(request,'pwd_reset.html',{'email':email})     
        return redirect('index')     
                    #因为<form>表单中的路径要是确定的，所以post函数另外定义一个类来完成 
class ModifyView(View):   
    """重置密码post部分"""  
    def post(self,request):     
        reset_form=ResetForm(request.POST)     
        if reset_form.is_valid():       
            pwd1=request.POST.get('newpwd1','')       
            pwd2=request.POST.get('newpwd2','')       
            email=request.POST.get('email','')       
            if pwd1!=pwd2:         
                return render(request,'pwd_reset.html',{'msg':'密码不一致！'})       
            else:         
                user=Students.objects.get(email=email)         
                user.password=make_password(pwd2)         
                user.save()         
                return redirect('index')     
        else:       
            email=request.POST.get('email','')       
            return render(request,'pwd_reset.html',{'msg':reset_form.errors}) 
