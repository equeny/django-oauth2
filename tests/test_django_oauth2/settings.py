#-*- coding: utf-8 -*-

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
    'django.contrib.sites',
    'django.contrib.sessions',
    'test_django_oauth2',
    'django_oauth2',
)
