#-*- coding: utf-8 -*-
import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2.models import Client
from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings

class TestViewsAuthorizeInvalid(test_django_oauth2.TestCase):
    
    def get(self, data):
        return self.client.get(reverse('django_oauth2_authorize'), data=data)
    
    def test_no_response_type(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        data = {
            'client_id': c.key,
            'redirect_uri': redirect_uri,
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='invalid_request',
        )
    
    def test_invalid_response_type(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        data = {
            'response_type': 'foobar',
            'client_id': c.key,
            'redirect_uri': redirect_uri,
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='invalid_request',
        )
    
    def test_unsupported_response_type(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        backup = appsettings.RESPONSE_TYPES
        try:
            appsettings.RESPONSE_TYPES = (appconsts.RESPONSE_TYPE_TOKEN, )
            data = {
                'response_type': appconsts.RESPONSE_TYPE_CODE,
                'client_id': c.key,
                'redirect_uri': redirect_uri,
            }
            self.assertAuthorizeError(
                response=self.get(data),
                redirect_uri=redirect_uri,
                error='unsupported_response_type',
            )
        finally:
            appsettings.RESPONSE_TYPES = backup
    
    def test_no_client_id(self):
        redirect_uri = 'http://www.google.fr'
        data = {
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
            'redirect_uri': redirect_uri,
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='invalid_request',
        )

    def test_invalid_client_id(self):
        redirect_uri = 'http://www.google.fr'
        Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        data = {
            'response_type': appconsts.RESPONSE_TYPE_CODE,
            'client_id': 'quinexistepas',
            'redirect_uri': redirect_uri,
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='invalid_client',
        )

    def test_no_redirect_uri(self):
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES,
        )
        data = {
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_TOKEN,
        }
        response = self.get(data)
        self.assertEquals(400, response.status_code)
        self.assertEquals('No redirect_uri to send response.', response.content)

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
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='redirect_uri_mismatch',
        )

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
        response = self.get(data)
        self.assertEquals(400, response.status_code)
        self.assertEquals('Absolute redirect_uri required.', response.content)

    def test_unauthorized_client(self):
        redirect_uri = 'http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=(appconsts.RESPONSE_TYPE_TOKEN, ),
        )
        data = {
            'redirect_uri': redirect_uri,
            'client_id': c.key,
            'response_type': appconsts.RESPONSE_TYPE_CODE,
        }
        self.assertAuthorizeError(
            response=self.get(data),
            redirect_uri=redirect_uri,
            error='unauthorized_client',
        )

if __name__ == '__main__':
    test_django_oauth2.main()
    