#-*- coding: utf-8 -*-
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from django_oauth2.conf import settings as oauth2_settings

def load_backend(path):
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing OAuth 2.0 authentication backend %s: "%s"' % (module, e))
    except ValueError, e:
        raise ImproperlyConfigured('Error importing OAuth 2.0 authentication backend. Is OAUTH2_AUTHENTICATION_BACKEND a correctly defined string?')
    try:
        cls = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" OAuth 2.0 authentication backend' % (module, attr))
    return cls()

def authenticate(request, authorization_request):
    return load_backend(oauth2_settings.AUTHENTICATION_BACKEND).authenticate(request, authorization_request)
