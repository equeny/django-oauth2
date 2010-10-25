#-*- coding: utf-8 -*-
import test_django_oauth2
import urllib

from django.core.urlresolvers import reverse

from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings
from django_oauth2.models import Client, AccessRange, Code

class TestTokenCodeInvalid(test_django_oauth2.TestCase):
    
    def process(self, data, post=True, content_type='application/x-www-form-urlencoded'):
        if post:
            return self.client.post(
                reverse('django_oauth2_token'),
                data=urllib.urlencode(data),
                content_type=content_type
            )
        else:
            return self.client.get(
                reverse('django_oauth2_token'),
                data=urllib.urlencode(data)
            )

    def test_get(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data, post=False), error='invalid_request')

    def test_invalid_content_type(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data, content_type='foobar'), error='invalid_request')
    
    def test_no_grant_type(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')
    
    def test_invalid_grant_type(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': 'foobar',
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_no_client_id(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_invalid_client_id(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': 'quinexistepas',
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_no_code(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_invalid_code(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': 'quinexistepas',
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_no_redirect_uri(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_invalid_redirect_uri(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': '/foobar',
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_no_client_secret(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    def test_invalid_client_secret(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': 'badsecret',
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenError(self.process(data), error='invalid_request')

    

if __name__ == '__main__':
    test_django_oauth2.main()
    