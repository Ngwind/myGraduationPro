from django.contrib import admin
from .models import Course, Video, CourseProgress, Scores


# 视频观看进度
@admin.register(CourseProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('video', 'student', 'editdate', 'progress')
    search_fields = ('video', 'student')
    ordering = ('video', 'student')
    readonly_fields = ['progress', 'editdate', 'video', 'student']

    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


# 课程
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseName', 'publisher', 'createdate')

    def get_queryset(self, request):
        """函数作用：使当前登录的普通用户只能看到自己负责的课程"""
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


# 视频
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('videoName', 'chapterId', 'videoUrl', 'course', 'publisher', 'createdate', 'editdate')
    search_fields = ['videoName', 'course', 'publisher']
    list_filter = ['publisher', 'course']
    ordering = ['publisher', 'course', 'chapterId']

    def get_queryset(self, request):
        """函数作用：使当前登录的普通用户只能看到自己添加的课程"""
        qs = super(VideoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


# 成绩
@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'score')
    search_fields = ['student', 'course']
    ordering = ['course', 'score']

    def get_queryset(self, request):
        """函数作用：当前登录的普通用户只能看到自己课程的成绩"""
        qs = super(ScoresAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(course__in=(Course.objects.filter(publisher=request.user)).values('id'))


admin.site.site_header = 'GDUT在线教学管理系统'
admin.site.site_title = '教务管理'
