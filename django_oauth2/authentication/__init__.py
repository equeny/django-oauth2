#-*- coding: utf-8 -*-
from django.utils.importlib import import_module
from django.core.exceptions import ImproperlyConfigured

from django_oauth2 import settings as appsettings

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
    return load_backend(appsettings.AUTHENTICATION_BACKEND).authenticate(request, authorization_request)
