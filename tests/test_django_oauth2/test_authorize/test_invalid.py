#-*- coding: utf-8 -*-
import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings
from django_oauth2.models import Client, AccessRange

class TestAuthorizeInvalid(test_django_oauth2.TestCase):
    
    def get(self, data):
        return self.client.get(reverse('django_oauth2_authorize'), data=data)
    
    def test_no_response_type(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        data = {
            'client_id': c.key,
            'redirect_uri': 'http://www.google.fr'
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=
            error='invalid_request')
    
    def test_invalid_response_type(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        data = {
            'response_type': 'foobar',
            'client_id': c.key,
            'redirect_uri': 'http://www.google.fr'
        }
        self.assertAuthorizeError(data, error='invalid_request')
    
    def test_unsupported_response_type(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        backup = appsettings.RESPONSE_TYPES
        try:
            appsettings.RESPONSE_TYPES = (appconsts.RESPONSE_TYPE_TOKEN, )
            data = {
                'response_type': appconsts.RESPONSE_TYPE_CODE,
                'client_id': c.key,
                'redirect_uri': 'http://www.google.fr'
            }
            self.assertAuthorizeError(data, error='unsupported_response_type')
        finally:
            appsettings.RESPONSE_TYPES = backup
    
    def test_no_client_id(self):
        data = {
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
            'redirect_uri': 'http://www.google.fr'
        }
        self.assertAuthorizeError(data, error='invalid_request')

    def test_invalid_client_id(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        data = {
            'response_type': appconsts.RESPONSE_TYPE_CODE,
            'client_id': 'quinexistepas',
            'redirect_uri': 'http://www.google.fr'
        }
        self.assertAuthorizeError(data, error='invalid_request')

    def test_no_redirect_uri(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        data = {
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
        }
        self.assertAuthorizeError(data, error='invalid_request')

    def test_redirect_uri_mismatch(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
            redirect_uri=redirect_uri,
        )
        data = {
            'redirect_uri': 'http://www.shiningpanda.com',
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
        }
        self.assertAuthorizeError(data, error='redirect_uri_mismatch', redirect_uri=redirect_uri)

    def test_relative_redirect_uri(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        data = {
            'redirect_uri': '/foobar',
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
        }
        self.assertAuthorizeError(data, error='invalid_request')

    def test_unauthorized_client(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=(appconsts.RESPONSE_TYPE_TOKEN, ),
        )
        data = {
            'redirect_uri': 'http://www.google.fr',
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_CODE,
        }
        self.assertAuthorizeError(data, error='unauthorized_client')

if __name__ == '__main__':
    test_django_oauth2.main()
    