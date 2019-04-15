from django.shortcuts import render
from django.http import HttpResponse
from wechatpy.oauth import WeChatOAuth, WeChatOAuthException
from .models import Scores, Video, CourseProgress, Course
from users.models import Openid, Student
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
        context['studentid'] = studentid
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
                context['studentid'] = op.studentid.studentId
                return render(request, "courses/courselist.html", context)
        except Exception:
            return no_login(request)


# 返回视频观看页面
def re_video_list(request):
    studentid = request.GET.get('studentid')
    courseid = request.GET.get('courseid')
    context = {"videos": []}
    if request.method == "GET" and studentid and courseid:
        try:
            course = Course.objects.get(pk=courseid)
        except Exception:
            return HttpResponse(status=404)

        for v in Video.objects.filter(course=course):
            t = CourseProgress.objects.get_or_create(defaults={'progress': '0%'}, video=v, student=Student.objects.get(studentId=studentid))
            print(t)
            time_s = t[0].progress  # 观看进度
            context['videos'].append([v, time_s])  # 保存video和观看进度到context
        context['studentid'] = studentid
        return render(request, "courses/learning.html", context)

    else:
        return HttpResponse(status=403)


# 获取前端视频vid，返回url字符串
def re_video_url(request):
    videoid = request.GET.get("vid")
    if videoid and request.method == "GET":
        try:
            vurl = Video.objects.get(pk=videoid).videoUrl
            print(vurl)
            return HttpResponse(vurl)
        except Exception:
            return HttpResponse("")
    return HttpResponse(status=403)


# 获取前端studentid、vid、观看进度，返回进度结果
def re_learn_progress(request):
    studentid = request.GET.get("studentid")
    videoid = request.GET.get("vid")
    now_t = request.GET.get("nt")
    dur_t = request.GET.get("dt")
    if request.method == "GET" and studentid and videoid and now_t and dur_t:
        if is_login(studentid):
            try:
                f_p = float(now_t[0:len(now_t)-1]) / float(dur_t[0:len(dur_t)-1]) * 100
                if f_p == 100:
                    s_p = "100%"
                else:
                    s_p = str(round(f_p, 2))+"%"
                cp = CourseProgress.objects.filter(video__pk=videoid, student__studentId=studentid)
                cp_s = cp[0].progress
                if float(cp_s[0:len(cp_s)-1]) <= f_p:
                    cp.update(progress=s_p)
                else:
                    return HttpResponse(cp_s)
                return HttpResponse(s_p)
            except Exception:
                return HttpResponse("error")
        else:
            return HttpResponse("nologin")
    return HttpResponse(403)
