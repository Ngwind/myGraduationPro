from django.shortcuts import render, render_to_response
from django.http import HttpResponse


def index(request):

    return HttpResponse(request.path)


def login(request):
    """返回静态登录页面或者重定向到个人中心"""
    """先拿到微信服务器发来的openid，然后去数据库查询有没有这个数据，如果有就重定向到个人中心"""
    pass
    return render(request, "login.html", context={})


def user_center(request):
    """接受一个表单，校验登录"""
    return HttpResponse('登录成功！')

