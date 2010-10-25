from django.http import HttpResponse
from django_oauth2.resource import AccessTokenProvider


class OAuth2Authentication(object):

    def __init__(self):
        pass

    def is_authenticated(self, request):
        return AccessTokenProvider(request).process() is None
        
    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'OAuth realm="foobar"'
        resp.status_code = 401
        return resp


    