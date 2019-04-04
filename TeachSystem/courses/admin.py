from django.contrib import admin
from .models import Course, Video, CourseProgress, Scores


@admin.register(CourseProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('video', 'student', 'editdate', 'progress')
    # list_editable = ['progress']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseName', 'createdate', 'publisher')

    def get_queryset(self, request):
        """函数作用：使当前登录的用户只能看到自己负责的学生"""
        qs = super(CourseAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(publisher=request.user)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('videoName', 'chapterId', 'videoUrl', 'course', 'publisher', 'createdate', 'editdate')


@admin.register(Scores)
class ScoresAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'score')
