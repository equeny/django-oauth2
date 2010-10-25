#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *    # pylint: disable-msg=W0401,W0614

# Get the administration site
from django.contrib import admin
admin.autodiscover()

# Define DEBUG URLs
debug = patterns('',
    # Get MEDIA (debug only, use APACHE configuration in production)
    (r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, }),
)

# Define productions URLs
production = patterns('',
    # Get the administration site
    (r'^admin/(.*)', admin.site.root),
    # General tools
    (r'oauth2/', include('django_oauth2.urls')),
    # General tools
    (r'client/', include('client.urls')),
    # General tools
    (r'api/', include('api.urls')),
)

# Get the right URL pattern
if settings.DEBUG:
    # Enable DEBUG
    urlpatterns = debug
    # Add production
    urlpatterns += production
# Production only
else: urlpatterns = production
