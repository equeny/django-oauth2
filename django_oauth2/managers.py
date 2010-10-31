from django.db import models

from django_oauth2 import settings as appsettings
from django_oauth2 import consts as appconst
from django_oauth2.tools import generate_unique_key, generate_timestamp

class ClientManager(models.Manager):
    
    def create(self, key, name, authorized_reponse_types, secret=None, description=None, redirect_uri=None):
        client = self.model(
            key=key,
            name=name,
            description=description,
            redirect_uri=redirect_uri,
            )
        client.authorize_response_types(*authorized_reponse_types)
        if secret:
            client.set_secret(secret)
        else:
            client.set_unusable_secret()
        client.save()
        return client

class AuthorizationRequestManager(models.Manager):
    
    def create(self, response_type, client, redirect_uri=None, state=None, scope=None, expire=None):
        key = generate_unique_key(
            self.model,
            key_length=appconst.AUTHORIZATION_REQUEST_KEY_LENGTH,
            )
        authorization_request = self.model(
            key = key,
            response_type = response_type,
            client = client,
            redirect_uri = redirect_uri,
            state = state,
            expire = expire or generate_timestamp(appsettings.AUTHORIZATION_REQUEST_EXPIRY),
            #scope = ' '.join(scope),
            )
        authorization_request.save()
        return authorization_request

class CodeManager(models.Manager):

    def create(self, user, client, redirect_uri, scope=None, expire=None):
        key = generate_unique_key(
            self.model,
            key_length=appconst.CODE_KEY_LENGTH,
            )
        code = self.model(
            key = key,
            client = client,
            active=True,
            expire = expire or generate_timestamp(appsettings.CODE_EXPIRY),
            redirect_uri = redirect_uri,
            #scope = scope,
            user = user,
            )
        code.save()
        return code

class AccessTokenManager(models.Manager):

    def create(self, user, client, refreshable=False, expire=None):
        token = generate_unique_key(
            self.model,
            key_length=appconst.ACCESS_TOKEN_LENGTH,
            key_field='token',
            )
        refresh_token = None
        if refreshable and appsettings.ALLOW_REFRESH_TOKEN:
            refresh_token = generate_unique_key(
                self.model,
                key_length=appconst.REFRESH_TOKEN_LENGTH,
                key_field='refresh_token',
            )
        access_token = self.model(
            token = token,
            refresh_token = refresh_token,
            expire = expire or generate_timestamp(appsettings.ACCESS_TOKEN_EXPIRY),
            client=client,
            user = user,
            )
        access_token.save()
        return access_token

class AccessRangeManager(models.Manager):
    pass