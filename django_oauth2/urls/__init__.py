#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include

from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings

# Add end-points
urlpatterns = patterns('',
    (r'', include('django_oauth2.urls.oauth2')),
)

# Add errors URI
if appsettings.ERROR_URI:
    urlpatterns += patterns('',
        (r'', include('django_oauth2.urls.errors')),
    )

# Add core authentication
if appsettings.AUTHENTICATION_BACKEND == appconsts.AUTHENTICATION_BACKEND_CORE:
    urlpatterns += patterns('',
        (r'', include('django_oauth2.urls.authentication')),
    )
