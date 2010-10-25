#-*- coding: utf-8 -*-
from django.http import HttpResponse

def handle_home(request):
    return HttpResponse('<h1>It works!</h1>')