#-*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    # Test
    (r'', include('django_oauth2.urls.authentication')),
    # Services
    (r'', include('django_oauth2.urls.errors')),
    # API JavaScripts
    (r'', include('django_oauth2.urls.oauth2')),
)
