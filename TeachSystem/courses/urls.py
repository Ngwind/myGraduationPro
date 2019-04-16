from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("courselist/", views.re_course_list, name="courselist"),
    path("learning/", views.re_video_list, name="learning"),
    path("getvurl/", views.re_video_url, name="getvurl"),
    path("setprogress/", views.re_learn_progress, name="progress"),
    path("coursescore/", views.re_course_score, name="score"),
]
