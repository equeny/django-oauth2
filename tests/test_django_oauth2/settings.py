#-*- coding: utf-8 -*-
import os

# Database connection info.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

# Site.
SITE_ID = 1

# URLs.
ROOT_URLCONF = 'test_django_oauth2.urls'

# List of strings representing installed apps.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django_oauth2',
)

# List of locations of the template source files, in search order.
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'),                 
)