#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def handle(request):
    return render_to_response('client.html', RequestContext(request, {}))