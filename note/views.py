from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note

# Create your views here.

# 定义一个装饰器检测用户是否登录
def login_check(func):
    def execute_view(request, *args, **kwargs):
        # 在执行视图函数前检测用户是否登录，如果没有用户数据，则重定向到登录页面
        if 'uname' not in request.session and 'uid' not in request.session:
            return HttpResponseRedirect('/user/login')

        return func(request, *args, **kwargs)
    return execute_view

@login_check
def list_view(request):
    uid = request.session['uid']
    uname = request.session['uname']
    notes = Note.objects.filter(user_id=uid)
    return render(request, 'note/list_note.html', locals())

@login_check
def add_view(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        uid = request.session['uid']
        if not title or not content:
            return HttpResponse('标题或内容不能为空，<a href="/note/add/">返回</a>')

        try:
            Note.objects.create(title=title, content=content, user_id=uid)

        except:
            return HttpResponse('添加失败，<a href="/note/add/">返回</a>')

        return HttpResponseRedirect('/note/')

@login_check
def mod_view(request, id):
    if request.method == 'GET':
        note = Note.objects.get(id=id)
        return render(request, 'note/mod_note.html', locals())
    elif request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if not title or not content:
            return HttpResponse('标题或内容不能为空<a href="/note/add/"></a>')

        note = Note.objects.get(id=id)
        note.title = title
        note.content = content
        note.save()

        return HttpResponseRedirect('/note/')

@login_check
def del_view(request, id):
    note = Note.objects.get(id=id)
    note.delete()
    return HttpResponseRedirect('/note/')