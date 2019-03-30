from django.contrib import admin
from .models import Course, Video, CourseProgress, Scores


admin.site.register(Course)
admin.site.register(Video)
admin.site.register(CourseProgress)
admin.site.register(Scores)



