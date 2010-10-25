#-*- coding: utf-8 -*-
from django.http import HttpResponse

from django_oauth2.decorators import resource

@resource
def handle(request):
    return HttpResponse('ok')