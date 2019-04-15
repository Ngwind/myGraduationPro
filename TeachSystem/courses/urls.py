from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="a"),
    path("courselist/", views.re_course_list, name="courselist"),
    path("learning/", views.re_video_list, name="learning"),
]
