#-*- coding: utf-8 -*-
import test_django_oauth2

from django_oauth2 import consts as appconsts
from django_oauth2.models import Client, AuthorizationRequest
from django_oauth2.views.authorize import authorization_deny_response

class TestViewsAuthorizeDeny(test_django_oauth2.TestCase):
    
    def test(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            key='test',
            name='test client',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        r = AuthorizationRequest.objects.create(
            response_type=appconsts.RESPONSE_TYPE_TOKEN,
            client=c,
            redirect_uri=redirect_uri,
        )
        response = authorization_deny_response(r)
        self.assertAuthorizeError(
            response,
            redirect_uri=redirect_uri,
            error='access_denied',
        )

if __name__ == '__main__':
    test_django_oauth2.main()
    