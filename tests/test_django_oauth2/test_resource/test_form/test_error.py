#-*- coding: utf-8 -*-
import test_django_oauth2
import urllib

from django.core.urlresolvers import reverse

from django_oauth2 import consts as appconsts
from django_oauth2 import settings as appsettings
from django_oauth2.models import Client, AccessToken

class TestTokenCodeInvalid(test_django_oauth2.TestCase):
    
    def process(self, data, content_type='application/x-www-form-urlencoded'):
        if data:
            data = urllib.urlencode(data)
        return self.client.post(reverse('resource'), data=data, content_type=content_type)

    def test_no_token(self):
        response = self.process({})
        self.assertEquals(401, response.status_code)
        self.assertEquals("OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM, response['WWW-Authenticate'])

    def test_invalid_content_type(self):
        access_token = AccessToken.objects.create(refreshable=True)
        response = self.process({'oauth_token': access_token.token, })
        self.assertEquals(401, response.status_code)
        self.assertEquals("OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM, response['WWW-Authenticate'])

    def test_invalid_token(self):
        access_token = AccessToken.objects.create(refreshable=True)
        response = self.process({'oauth_token': access_token.token, })
        self.assertEquals(401, response.status_code)
        self.assertEquals("OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM, response['WWW-Authenticate'])

    def test_expired_token(self):
        access_token = AccessToken.objects.create(refreshable=True)
        response = self.process({'oauth_token': access_token.token, })
        self.assertEquals(401, response.status_code)
        self.assertEquals("OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM, response['WWW-Authenticate'])


if __name__ == '__main__':
    test_django_oauth2.main()
    