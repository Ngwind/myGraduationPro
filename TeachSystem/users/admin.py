from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('studentId', 'username', 'college', 'userclass', 'createdate')
    search_fields = ['studentId', 'username', 'college', 'userclass']
    list_filter = ['college', 'userclass']
    ordering = ('college', 'userclass', 'studentId')
    # list_editable = ['college', 'userclass']


admin.site.register(Teacher, UserAdmin)

