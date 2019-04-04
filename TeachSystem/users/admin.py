from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student
from courses.models import CourseProgress, Video # 忽略这些红色波浪线，其实是正确的


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentId', 'username', 'college', 'userclass', 'createdate')
    search_fields = ['studentId', 'username', 'college', 'userclass']
    list_filter = ['college', 'userclass']
    ordering = ('college', 'userclass', 'studentId')
    readonly_fields = ['studentId', 'username', 'college', 'userclass', 'createdate', 'password', 'gender']
    # list_editable = ['college', 'userclass']

    def get_queryset(self, request):
        """限定普通用户只能看到自己学生的信息"""
        qs = super(StudentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(studentId__in=(CourseProgress.objects.filter(video__in=Video.objects.filter(publisher=request.user).values('id'))).values('student'))

    def get_readonly_fields(self, request, obj=None):
        """设置普通用户不能编辑学生信息"""
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields


admin.site.register(Teacher, UserAdmin)
