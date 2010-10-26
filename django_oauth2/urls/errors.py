#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    # Authorize errors
    url(r'^error/authorize/(?P<error>.+)/$', 'django_oauth2.views.authorize.handle_error', name='django_oauth2_authorize_error'),
    # Token errors
    url(r'^error/token/(?P<error>.+)/$'    , 'django_oauth2.views.token.handle_error'    , name='django_oauth2_token_error'    ),
    # Resource errors
    url(r'^error/resource/(?P<error>.+)/$' , 'django_oauth2.views.resource.handle_error' , name='django_oauth2_resource_error' ),
)
