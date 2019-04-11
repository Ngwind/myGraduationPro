from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Student


def index(request):

    return HttpResponse(request.path)


def login(request):
    """返回静态登录页面或者重定向到个人中心"""
    """先拿到微信服务器发来的openid，然后去数据库查询有没有这个数据，如果有就重定向到个人中心"""
    tipsflag = {'loginflag': '0'}
    if request.method == "GET":
        pass
    elif request.method == "POST":
        # 验证密码账号
        check = False
        studentid = request.POST.get('studentid')
        password = request.POST.get('password')
        try:
            s = Student.objects.get(studentId=studentid, password=password)
            check = True
        except ObjectDoesNotExist:
            print("loginerror")
            check = False
        if check:
            # 登录成功
            userinfo = {"s": s}
            return HttpResponse('welcome!')  # render(request, "user_center.html", userinfo)
        else:
            # 登录失败
            tipsflag['loginflag'] = '1'
    return render(request, "users/login.html", tipsflag)


def user_center(request):
    """接受一个表单，校验登录"""
    return HttpResponse('登录成功！')

