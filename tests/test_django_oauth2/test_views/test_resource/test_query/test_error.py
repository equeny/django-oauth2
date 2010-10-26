#-*- coding: utf-8 -*-
import urllib

import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2.models import AccessToken
from django_oauth2 import settings as appsettings

class TestViewsResourceQueryError(test_django_oauth2.TestCase):
    
    def process(self, qs, data=None):
        if data is not None:
            return self.client.post('%s?%s' (reverse('resource'), urllib.urlencode(qs)), data)
        else:
            return self.client.get(reverse('resource'), qs)

    #def test(self):
    #    access_token = AccessToken.objects.create(refreshable=True)
    #    response = self.process({})
    #    self.assertEquals(401, response.status_code)
    #    self.assertEquals("OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM, response['WWW-Authenticate'])


if __name__ == '__main__':
    test_django_oauth2.main()
    