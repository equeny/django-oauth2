#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',  

    # -------------------------------------------------------------------------
    # MEDIA ACCESS
    # -------------------------------------------------------------------------
    # Check that allowed before serving the media files 
    url(r'^authorize/$', 'django_oauth2.authorization.authorization_request', name='django_oauth2_authorize'),
    
    url(r'^error/authorize/(?P<error>.+)/$', 'django_oauth2.authorize.handle_error', name='django_oauth2_authorize_error'),
    url(r'^error/token/(?P<error>.+)/$', 'django_oauth2.token.handle_error', name='django_oauth2_token_error'),
    url(r'^error/access/(?P<error>.+)/$', 'django_oauth2.access.handle_error', name='django_oauth2_access_error'),

    url(r'^token/$', 'django_oauth2.token.access_token', name='django_oauth2_token'),

    url(r'^authenticate/core/$', 'django_oauth2.authentication.core.handle', name='django_oauth2_authenticate_core'),

)
