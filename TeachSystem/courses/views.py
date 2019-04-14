from django.shortcuts import render
from wechatpy.oauth import WeChatOAuth, WeChatOAuthException
from .models import Scores, Video, CourseProgress
from users.models import Openid
from users.views import no_login, is_login


def index(request):
    return render(request, "courses/testvideo.html")


# 通用openid获取函数
def get_openid(request):
    if request.method == "GET":
        code = request.GET.get('code')
        if code:
            app_id = 'wx425d2aedb363e9c6'
            app_sercet = '57a89d10bbb0754f07b75825491b627e'
            r_url = 'https://www.gdutwuenda.cn/course/learning/'
            wco = WeChatOAuth(app_id, app_sercet, r_url, scope='snsapi_base', state='123')
            try:
                json_oauth = wco.fetch_access_token(code)
                return json_oauth['openid']
            except WeChatOAuthException:  # 考虑code被重复使用的情况，重定向到用户登录-微信授权url
                pass
    return "error"


# 返回课程list页面
def re_course_list(request):
    context = {'Courses': []}
    studentid = request.GET.get('studentid')

    if studentid and is_login(studentid):  # 个人中心转跳,拿studentid
        for s in Scores.objects.filter(student__studentId=studentid):
            c = s.course
            stu = s.student
            t = Video.objects.filter(course=c).count()
            per_sum = 0
            for l in CourseProgress.objects.filter(student=stu, video__course=c):
                str_p = l.progress
                per_sum += float(str_p[0: len(str_p) - 1])
            try:
                complate_per = round(per_sum / t, 2)
            except ZeroDivisionError:
                complate_per = round(0, 2)
            context['Courses'].append([c, complate_per])  # 保存student的所有course
        return render(request, "courses/courselist.html", context)

    else:  # 公众号菜单转跳,拿openid
        openid = get_openid(request)
        try:
            op = Openid.objects.get(openid=openid)
            if openid != "error":  # 验证登录有效
                for s in Scores.objects.filter(student=op.studentid):
                    c = s.course
                    stu = s.student
                    t = Video.objects.filter(course=c).count()
                    per_sum = 0
                    for l in CourseProgress.objects.filter(student=stu, video__course=c):
                        str_p = l.progress
                        per_sum += float(str_p[0: len(str_p)-1])
                    try:
                        complate_per = round(per_sum/t, 2)
                    except ZeroDivisionError:
                        complate_per = round(0, 2)
                    context['Courses'].append([c, complate_per])

                return render(request, "courses/courselist.html", context)
        except Exception:
            return no_login(request)


