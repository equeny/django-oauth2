#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url   # pylint: disable-msg=W0401,W0614

# Define DEBUG URLs
debug = patterns('')

# Define productions URLs
production = patterns('',
    # Home page
    url(r'^$', 'example.client.views.handle_home', name='client'),

)

# Get the right URL pattern
if settings.DEBUG:
    # Enable DEBUG
    urlpatterns = debug
    # Add production
    urlpatterns += production
# Production only
else: urlpatterns = production
