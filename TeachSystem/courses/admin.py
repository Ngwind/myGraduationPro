from django.contrib import admin
from .models import Course, Video, CourseProgress, Scores


@admin.register(CourseProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('video', 'student', 'editdate', 'progress')
    search_fields = ('video', 'student')
    ordering = ('video', 'student')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseName', 'publisher', 'createdate')

    def get_queryset(self, request):
        """函数作用：使当前登录的普通用户只能看到自己负责的课程"""
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


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


@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'score')
    search_fields = ['student', 'course']
    ordering = ['course', 'score']

