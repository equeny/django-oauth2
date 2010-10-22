
from django.db import models
from django.contrib.auth.models import User

from django_oauth2 import consts as oauth2_consts
from django_oauth2.managers import ClientManager, CodeManager, AccessTokenManager, AccessRangeManager, AuthorizationRequestManager
from django_oauth2.tools import normalize_redirect_uri


class Client(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField(blank=True)
    key = models.CharField(unique=True, max_length=oauth2_consts.CLIENT_KEY_LENGTH)
    secret = models.CharField(unique=True, max_length=oauth2_consts.CLIENT_SECRET_LENGTH)
    redirect_uri = models.URLField(null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True, related_name='clients')
    authorized_reponse_types = models.PositiveIntegerField(choices=oauth2_consts.AUTHORIZED_RESPONSE_TYPE_CHOICES, default=0)
    objects = ClientManager()

    def match_redirect_uri(self, redirect_uri):
        return normalize_redirect_uri(redirect_uri) == normalize_redirect_uri(self.redirect_uri)
    
    def is_authorized_response_type(self, response_type):
        return self.authorized_reponse_types & oauth2_consts.RESPONSE_TYPE_BITS.get(response_type, 0) != 0

    def authorize_response_types(self, *response_types):
        bit = 0
        for response_type in list(set(response_types)):
            bit |= oauth2_consts.RESPONSE_TYPE_BITS.get(response_type, 0)
        self.authorized_reponse_types = bit


class AccessRange(models.Model):
    
    key = models.CharField(unique=True, max_length=256)
    description = models.TextField(blank=True)
    
    objects = AccessRangeManager()

    def __unicode__(self):
        return self.key

class AuthorizationRequest(models.Model):
    key = models.CharField(max_length=oauth2_consts.AUTHORIZATION_REQUEST_KEY_LENGTH)
    response_type = models.CharField(max_length=256, choices=oauth2_consts.RESPONSE_TYPE_CHOICES)
    client = models.ForeignKey(Client)
    redirect_uri = models.URLField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    timestamp = models.PositiveIntegerField()
    #scope = models.ManyToManyField(AccessRange)
    scope = models.TextField(null=True, blank=True)
    
    objects = AuthorizationRequestManager()

class AccessToken(models.Model):
    objects = AccessTokenManager()
    token = models.CharField(max_length=oauth2_consts.ACCESS_TOKEN_LENGTH)
    refresh_token = models.CharField(blank=True, null=True, max_length=oauth2_consts.REFRESH_TOKEN_LENGTH)
    timestamp = models.PositiveIntegerField()

class ClientUser(models.Model):
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User)
    scope = models.ManyToManyField(AccessRange)

class Code(models.Model):
    objects = CodeManager()
    key = models.CharField(max_length=oauth2_consts.AUTHORIZATION_REQUEST_KEY_LENGTH)
    active = models.BooleanField(default=True)
    client = models.ForeignKey(Client)
    timestamp = models.PositiveIntegerField()
    redirect_uri = models.URLField(null=True, blank=True)
    scope = models.TextField(null=True, blank=True)

    def match_redirect_uri(self, redirect_uri):
        return normalize_redirect_uri(redirect_uri) == normalize_redirect_uri(self.redirect_uri)
    