#-*- coding: utf-8 -*-
import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings
from django_oauth2.models import Client, AuthorizationRequest
from django_oauth2.authorize import authorization_deny_response,\
    authorization_grant_response

class TestAuthorizeGrant(test_django_oauth2.TestCase):
    
    def test_token(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_TOKEN,
            client=c,
            redirect_uri='http://www.google.fr',
        )
        print authorization_grant_response(r, 'foobar')

    def test_code(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_CODE,
            client=c,
            redirect_uri='http://www.google.fr',
        )
        print authorization_grant_response(r, 'foobar')

    def test_code_and_token(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_CODE_AND_TOKEN,
            client=c,
            redirect_uri='http://www.google.fr',
        )
        print authorization_grant_response(r, 'foobar')

if __name__ == '__main__':
    test_django_oauth2.main()
    