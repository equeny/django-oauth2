#-*- coding: utf-8 -*-
# Django settings for pypid project.
import os
import warnings

# -----------------------------------------------------------------------------
# HELPERS
# -----------------------------------------------------------------------------
# Get the folder containing the project
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
# Get a path in folder tree
def example_home(*args):
    '''Get file path starting from ROOT_DIR'''
    return os.path.join(ROOT_DIR, *args)

# -----------------------------------------------------------------------------
# DJANGO CORE
# -----------------------------------------------------------------------------
# Debug flags.
DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Database connection info.
DATABASES = {
    'default': {
        'ENGINE'  : 'django.db.backends.sqlite3',
        'NAME'    : example_home('dbs', 'example.dbs'),   
        'USER'    : '',
        'PASSWORD': '',
        'HOST'    : '', 
        'PORT'    : '',
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Paris'

# Do not load I18N.
USE_I18N = False

# Site ID
SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '%s%s' % (example_home('static'), os.sep)

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/static/'

# A secret key for this particular Django installation. Used in secret-key
# hashing algorithms. Set this in your settings, or Django will complain
# loudly.
SECRET_KEY = 'vi(50i@g2+^jau7wawiqdl-q-rpw$*jt4@r%at663@+9kg1ge0'

# URLs.
ROOT_URLCONF = 'example.urls'

# List of strings representing installed apps.
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django_oauth2',
    'example.client',
    'example.api',
)

# List of locations of the template source files, in search order.
TEMPLATE_DIRS = (
    example_home('templates'),                 
)

# -----------------------------------------------------------------------------
# DJANGO MIDDLEWARE
# -----------------------------------------------------------------------------
# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.gzip.GZipMiddleware',
)

# -----------------------------------------------------------------------------
# LOCAL SETTINGS
# -----------------------------------------------------------------------------
try: from example.localsettings import *    # pylint: disable-msg=F0401,E0611
except ImportError: warnings.warn("skip example.localsettings as file doesn't exist")
