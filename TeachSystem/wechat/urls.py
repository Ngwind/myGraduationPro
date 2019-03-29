from django.urls import path
from . import views

urlpatterns = [
    path('', views.we_chat_main),
    path('testfunc/', views.test_func),
]
