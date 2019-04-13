from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path('moresettings/', views.more_settings, name="moresettings"),
    path('changepwd/', views.re_change_pwd, name="changepwd"),
    path('modpwd/', views.change_pwd, name="modpwd"),
    path("nologin/", views.no_login, name="nologin"),
]