#-*- coding: utf-8 -*-

class IBackend(object):
    
    def authenticate(self, request, authorization_request):
        raise NotImplementedError
