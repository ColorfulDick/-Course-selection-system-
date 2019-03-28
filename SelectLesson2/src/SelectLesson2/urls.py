"""SelectLesson2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
#from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from lesson import views
import xadmin
from lesson.views import ForgetPwdView,ResetView,ModifyView 

urlpatterns = [
    path('admin/',xadmin.site.urls),
    path('index/',views.index,name='index'),
    path('regist/',views.regist),
    path('login/',views.login),
    path('selectlesson/',views.selectlesson),
    path('logout/',views.logout),
    path('managelesson/',views.managelesson),
    path('video/', views.video),
    path('get_valid_img.png/', views.get_valid_img),
    path('forget/',ForgetPwdView.as_view(),name='forget_pwd'),   #÷ÿ÷√√‹¬Î   
    path('reset/<str:active_code>',ResetView.as_view(),name='reset'),   
    path('modify/',ModifyView.as_view(),name='modify'),
    path('captcha/',include('captcha.urls')), 
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
