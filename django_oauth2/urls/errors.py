#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

from django_oauth2 import settings as appsettings

if appsettings.ERROR_URI:
    urlpatterns = patterns('',
        url(r'^error/authorize/(?P<error>.+)/$', 'django_oauth2.authorize.handle_error', name='django_oauth2_authorize_error'),
        url(r'^error/token/(?P<error>.+)/$'    , 'django_oauth2.token.handle_error'    , name='django_oauth2_token_error'    ),
        url(r'^error/access/(?P<error>.+)/$'   , 'django_oauth2.resource.handle_error' , name='django_oauth2_resource_error' ),
    )
else: urlpatterns = ()