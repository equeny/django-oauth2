#-*- coding: utf-8 -*-
import test_django_oauth2

from django_oauth2 import consts as appconsts
from django_oauth2.views.authorize import authorization_grant_response
from django_oauth2.models import Client, AuthorizationRequest, AccessToken, Code

class TestViewsAuthorizeGrant(test_django_oauth2.TestCase):
    
    def test_token(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_TOKEN,
            client=c,
            redirect_uri=redirect_uri,
        )
        user = self.getuser()
        response = authorization_grant_response(r, user, 'foobar')
        self.assertAuthorizeGrantToken(
            response,
            redirect_uri,
            AccessToken.objects.get().token,
        )

    def test_code(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_CODE,
            client=c,
            redirect_uri=redirect_uri,
        )
        user = self.getuser()
        response = authorization_grant_response(r, user, 'foobar')
        self.assertAuthorizeGrantCode(
            response,
            redirect_uri,
            Code.objects.get().key,
        )

    def test_code_and_token(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_CODE_AND_TOKEN,
            client=c,
            redirect_uri=redirect_uri,
        )
        user = self.getuser()
        response = authorization_grant_response(r, user, 'foobar')
        self.assertAuthorizeGrantCodeToken(
            response,
            redirect_uri,
            Code.objects.get().key,
            AccessToken.objects.get().token,
        )

if __name__ == '__main__':
    test_django_oauth2.main()
    