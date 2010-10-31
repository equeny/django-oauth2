#-*- coding: utf-8 -*-
from django.db import models
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _

from django_oauth2 import managers
from django_oauth2 import consts as appconsts
from django_oauth2.tools import normalize_redirect_uri, generate_unique_key
from django_oauth2.db.fields import TimestampField, CreationTimestampField

UNUSABLE_SECRET = '!' # This will never be a valid hash

def get_hexdigest(algorithm, salt, raw_secret):
    raw_secret, salt = smart_str(raw_secret), smart_str(salt)
    if algorithm == 'ssha':
        import base64
        raw_salt = base64.b16decode(str.upper(salt))
        return sha_constructor(raw_secret + raw_salt).hexdigest()
    raise ValueError('Got unknown password algorithm type in password.')

class Client(models.Model):
    
    name = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    
    key = models.CharField(unique=True, max_length=appconsts.CLIENT_KEY_LENGTH)
    secret = models.CharField(_('secret'), unique=True, max_length=128, help_text=_("Use '[algo]$[salt]$[hexdigest]'."))
    
    redirect_uri = models.URLField(null=True, blank=True)
    
    #user = models.ForeignKey(User, null=True, blank=True, related_name='clients')
    authorized_reponse_types = models.PositiveIntegerField(choices=appconsts.AUTHORIZED_RESPONSE_TYPE_CHOICES, default=0)
    objects = managers.ClientManager()

    def match_redirect_uri(self, redirect_uri):
        return normalize_redirect_uri(redirect_uri) == normalize_redirect_uri(self.redirect_uri)
    
    def is_authorized_response_type(self, response_type):
        return self.authorized_reponse_types & appconsts.RESPONSE_TYPE_BITS.get(response_type, 0) != 0

    def authorize_response_types(self, *response_types):
        bit = 0
        for response_type in list(set(response_types)):
            bit |= appconsts.RESPONSE_TYPE_BITS.get(response_type, 0)
        self.authorized_reponse_types = bit

    def set_secret(self, raw_secret):
        import os, base64
        algo = 'ssha'
        salt = str.lower(base64.b16encode(os.urandom(4)))
        hsh = get_hexdigest(algo, salt, raw_secret)
        self.secret = '%s$%s$%s' % (algo, salt, hsh)

    def check_secret(self, raw_secret):
        algo, salt, hsh = self.secret.split('$')
        return hsh == get_hexdigest(algo, salt, raw_secret)

    def set_unusable_secret(self):
        self.secret = UNUSABLE_SECRET

    def has_usable_secret(self):
        return self.secret != UNUSABLE_SECRET


def getenerate_client_key():
    return generate_unique_key(Client, key_length=10, key_field='key')

class AccessRange(models.Model):
    
    key = models.CharField(unique=True, max_length=256)
    description = models.TextField(blank=True)
    
    objects = managers.AccessRangeManager()

    def __unicode__(self):
        return self.key

class AuthorizationRequest(models.Model):
    key = models.CharField(max_length=appconsts.AUTHORIZATION_REQUEST_KEY_LENGTH)
    response_type = models.CharField(max_length=256, choices=appconsts.RESPONSE_TYPE_CHOICES)
    redirect_uri = models.URLField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    issue = CreationTimestampField()
    expire = TimestampField()
    #scope = models.ManyToManyField(AccessRange)
    scope = models.TextField(null=True, blank=True)
    
    client = models.ForeignKey(Client)
    
    objects = managers.AuthorizationRequestManager()

class AccessToken(models.Model):
    objects = managers.AccessTokenManager()
    token = models.CharField(max_length=appconsts.ACCESS_TOKEN_LENGTH)
    refresh_token = models.CharField(blank=True, null=True, max_length=appconsts.REFRESH_TOKEN_LENGTH)
    issue = CreationTimestampField()
    expire = TimestampField()
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User, related_name='access_tokens')

#class ClientUser(models.Model):
#    client = models.ForeignKey(Client)
#    user = models.ForeignKey(User)
#    scope = models.ManyToManyField(AccessRange)

class Code(models.Model):
    objects = managers.CodeManager()
    key = models.CharField(max_length=appconsts.AUTHORIZATION_REQUEST_KEY_LENGTH)
    active = models.BooleanField(default=True)
    client = models.ForeignKey(Client)
    issue = CreationTimestampField()
    expire = TimestampField()
    redirect_uri = models.URLField(null=True, blank=True)
    scope = models.TextField(null=True, blank=True)
    client = models.ForeignKey(Client)
    user = models.ForeignKey(User, related_name='codes')

    def match_redirect_uri(self, redirect_uri):
        return normalize_redirect_uri(redirect_uri) == normalize_redirect_uri(self.redirect_uri)
    