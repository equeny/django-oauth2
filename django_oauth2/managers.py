import time
from django.db import models
from django.contrib.auth.models import User

from django_oauth2.conf import settings as oauth2_settings
from django_oauth2 import consts as oauth2_consts
from django_oauth2.tools import generate_unique_key_secret, generate_unique_key, generate_timestamp

class ClientManager(models.Manager):
    
    def create(self, name, authorized_reponse_types, description='', redirect_uri=None, user=None):
        key, secret = generate_unique_key_secret(
            self.model,
            key_length=oauth2_consts.CLIENT_KEY_LENGTH,
            secret_length=oauth2_consts.CLIENT_SECRET_LENGTH,
            )
        client = self.model(
            name=name,
            description=description,
            key=key,
            secret=secret,
            redirect_uri=redirect_uri,
            user=user,
            )
        client.authorize_response_types(*authorized_reponse_types)
        client.save()
        return client

class AuthorizationRequestManager(models.Manager):
    
    def create(self, response_type, client, redirect_uri=None, state=None, scope=None):
        key = generate_unique_key(
            self.model,
            key_length=oauth2_consts.AUTHORIZATION_REQUEST_KEY_LENGTH,
            )
        authorization_request = self.model(
            key = key,
            response_type = response_type,
            client = client,
            redirect_uri = redirect_uri,
            state = state,
            timestamp = generate_timestamp(),
            scope = ' '.join(scope),
            )
        authorization_request.save()
        return authorization_request

class CodeManager(models.Manager):

    def create(self, client, redirect_uri, scope=None):
        key = generate_unique_key(
            self.model,
            key_length=oauth2_consts.CODE_KEY_LENGTH,
            )
        code = self.model(
            key = key,
            client = client,
            active=True,
            timestamp = generate_timestamp(),
            redirect_uri = redirect_uri,
            scope = scope,
            )
        code.save()
        return code

class AccessTokenManager(models.Manager):

    def create(self, refreshable=True):
        token = generate_unique_key_secret(
            self.model,
            key_length=oauth2_consts.ACCESS_TOKEN_LENGTH,
            )
        refresh_token = None
        if refreshable and oauth2_settings.ALLOW_REFRESH_TOKEN:
            refresh_token = generate_unique_key_secret(
                self.model,
                key_length=oauth2_consts.REFRESH_TOKEN_LENGTH,
            )
        access_token = self.model(
            token = token,
            refresh_token = refresh_token,
            timestamp = generate_timestamp(),
            )
        access_token.save()
        return access_token

class AccessRangeManager(models.Manager):
    pass