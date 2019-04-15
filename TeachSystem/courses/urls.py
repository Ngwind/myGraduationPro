from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("courselist/", views.re_course_list, name="courselist"),
    path("learning/", views.index, name="learning"),
]
