#-*- coding: utf-8 -*-
from django.conf import settings

# Seconds
CODE_EXPIRY = getattr(settings, 'OAUTH2_CODE_EXPIRY', 120)

ACCESS_TOKEN_EXPIRY = getattr(settings, 'OAUTH2_ACCESS_TOKEN_EXPIRY', 3600)

AUTHENTICATION_BACKEND = getattr(settings, 'OAUTH2_AUTHENTICATION_BACKEND', 'django_oauth2.authentication.core.Backend')

AUTHORIZATION_ERRORS_VIEW = getattr(settings, 'OAUTH2_AUTHORIZATION_ERRORS_VIEW', 'django_oauth2_authorization_errors')

ACCESS_GRANT_BACKEND = getattr(settings, 'OAUTH2_ACCESS_GRANT_BACKEND', 'django_oauth2.grant.core.Backend')

ACCESS_TOKEN_EXPIRY = getattr(settings, 'OAUTH2_ACCESS_TOKEN_EXPIRY', 3600)

ALLOW_REFRESH_TOKEN = getattr(settings, 'OAUTH2_ALLOW_REFRESH_TOKEN', True)

AUTHENTICATE_REALM = getattr(settings, 'OAUTH2_AUTHENTICATE_REALM', None)

SCOPE_BACKEND = getattr(settings, 'OAUTH2_SCOPE_BACKEND', 'django_oauth2.scope.db.Backend')
