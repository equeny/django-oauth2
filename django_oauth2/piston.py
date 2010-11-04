#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django_oauth2.views.resource import AccessTokenProvider


class OAuth2Authentication(object):

    def __init__(self):
        pass

    def is_authenticated(self, request):
        return AccessTokenProvider(request).process() is None
        
    def challenge(self, request=None):
        '''
        Would be nice to get request object.
        '''
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'OAuth realm="foobar"'
        resp.status_code = 401
        return resp


    