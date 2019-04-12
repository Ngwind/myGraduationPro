from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Student, Openid
from wechatpy.oauth import WeChatOAuth, WeChatOAuthException

def index(request):

    return HttpResponse(request.path)


def login(request):
    """返回静态登录页面或者重定向到个人中心"""
    context = {'loginflag': '0',
               'openid': '0'}
    if request.method == "GET":
        code = request.GET.get('code')  # 先拿到微信服务器发来的openid，然后去数据库查询有没有这个数据，如果有就重定向到个人中心
        if code:
            app_id = 'wx425d2aedb363e9c6'
            app_sercet = '57a89d10bbb0754f07b75825491b627e'
            r_url = 'https://www.gdutwuenda.cn/user/login/'
            wco = WeChatOAuth(app_id, app_sercet, r_url, scope='snsapi_base', state='123')
            try:
                json_oauth = wco.fetch_access_token(code)
            except WeChatOAuthException:  # 考虑code被重复使用的情况，重定向到微信授权url
                print(wco.authorize_url)
                return HttpResponseRedirect(redirect_to=wco.authorize_url)

            openid = json_oauth['openid']
            try:  # 在数据库中校验有无openid对应的学生信息
                o = Openid.objects.get(openid=openid)
                s = o.studentid  # 获取openid对应的学生models对象
                userinfo = {"s": s}
                return HttpResponse('welcome by openid')  # render(request, "user_center.html", userinfo)
            except ObjectDoesNotExist:  # openid不在库中，当前用户是新用户，在openid表中记录
                context['openid'] = openid  # 模板中添加openid信息，返回给前端。用于POST方法时携带。
    elif request.method == "POST":
        # 验证密码账号
        studentid = request.POST.get('studentid')
        password = request.POST.get('password')
        openid = request.POST.get('openid')
        try:
            s = Student.objects.get(studentId=studentid, password=password)
            check = True
        except ObjectDoesNotExist:
            print("loginerror")
            check = False
        if check:
            # 登录成功
            if openid != '0':  # 判断一次，防止保存值为0的openid
                porc =  Openid.objects.update_or_create(openid=openid, studentid=s)  # 保存openid和账号信息。
            userinfo = {"s": s}
            return HttpResponse('welcome by password')  # render(request, "user_center.html", userinfo)
        else:
            # 登录失败
            context['loginflag'] = '1'
            context['openid'] = openid  # 再次带上openid
    return render(request, "users/login.html", context)


def user_center(request):
    """接受一个表单，校验登录"""
    return HttpResponse('登录成功！')

