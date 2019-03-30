from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Teacher, Student


admin.site.register(Teacher, UserAdmin)
admin.site.register(Student)

