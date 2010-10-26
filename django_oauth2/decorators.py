#-*- coding: utf-8 -*-
from django_oauth2.views.resource import handle_access_token

def resource(function=None):
    def decorator(request, *args, **kwargs):
        response = handle_access_token(request)
        if response:
            return response
        return function(request, *args, **kwargs)
    return decorator
        