from django.shortcuts import render, render_to_response
from django.http import HttpResponse


def index(request):

    return HttpResponse(request.path)


def login(request):
    """返回静态登录页面"""
    return render(request, "login.html", context={})


def check_login(request):
    """接受一个表单，校验登录"""
    pass

