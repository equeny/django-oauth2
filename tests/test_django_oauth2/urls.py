#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Define URLs
urlpatterns = patterns('',
    # OAuth2
    (r'', include('django_oauth2.urls')),
    # Resource
    url(r'^resource/$', 'test_django_oauth2.views.handle', name='resource'),
)
