#-*- coding: utf-8 -*-
from django.conf.urls.defaults import *

# Define productions URLs
urlpatterns = patterns('',
    # Registration
    (r'', include('django_oauth2.urls')),
)

