from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    openid = request.GET.get('openid', default=None)
    return HttpResponse(request.path+openid)
