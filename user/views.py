from django.http import HttpResponse
from django.shortcuts import render
from .models import User

# Create your views here.

def register_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_2 = request.POST.get('password_2')

        # 判断用户名和密码是否为空
        if not username or not password:
            return HttpResponse('用户名或密码不能为空')
            # 判断两次密码是否一致
        if password != password_2:
            return HttpResponse('两次密码不一致')
        # 与数据库交互，判断用户名在数据库中是否存在
        if User.objects.filter(username=username):
            return HttpResponse('用户名已存在')

        user = User.objects.create(username=username, password=password)
        return HttpResponse('用户注册成功，请 <a href="/user/login/">登录</a>')

def login_view(request):
    if request.method == 'GET':
        # 如果在访问login页面时有用户登录成功了，且session中有数据可以使用时，给用户一个特殊响应，不让用户访问登录模版
        if 'uname' in request.session and 'uid' in request.session:
            return HttpResponse(f'欢迎{request.session["uname"]}, 可访问其他功能或<a href="/user/logout">退出登录</a>')
        return render(request, 'user/login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            return HttpResponse('用户名和密码不能为空')

        try:
            user = User.objects.get(username=username)
        except:
            return HttpResponse('用户名或密码错误')
        if password != user.password:
            return HttpResponse('用户名或密码错误')

        # 保持登录状态
        request.session['uname'] = user.username
        request.session['uid'] = user.id

        return HttpResponse('登录成功，请 <a href="/note/">查看笔记</a>')

def logout_view(request):
    if 'uname' not in request.session and 'uid' not in request.session:
        return HttpResponse('未登录')
    del request.session['uname']
    del request.session['uid']

    return HttpResponse('退出登录成功')