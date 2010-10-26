#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Authorization end-point 
    url(r'^authorize/$', 'django_oauth2.views.authorize.handle_authorization_request', name='django_oauth2_authorize'),
    # Token end-point 
    url(r'^token/$'    , 'django_oauth2.views.token.handle_access_token'             , name='django_oauth2_token'    ),
)

