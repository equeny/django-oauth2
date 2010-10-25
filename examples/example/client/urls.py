#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url   # pylint: disable-msg=W0401,W0614

# Define productions URLs
urlpatterns = patterns('',
    # Home page
    url(r'^$', 'example.client.views.handle', name='client'),

)

