#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',  
    url(r'^authorize/$', 'django_oauth2.authorize.handle_authorization_request', name='django_oauth2_authorize'),
    url(r'^token/$'    , 'django_oauth2.token.handle_access_token'             , name='django_oauth2_token'    ),
)

