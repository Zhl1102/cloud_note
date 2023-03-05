from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.

# 定义一个装饰器检测用户是否登录
def login_check(func):
    def execute_view(request, *args, **kwargs):
        # 在执行视图函数前检测用户是否登录，如果没有用户数据，则重定向到登录页面
        if 'uname' not in request.session and 'uid' not in request.session:
            return HttpResponseRedirect('/user/login')

        func(request, *args, **kwargs)
    return execute_view

def list_view(request):
    pass

def add_view(request):
    pass

def mod_view(request):
    pass

def del_view(request):
    pass