#-*- coding: utf-8 -*-
import urllib

import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2.models import AccessToken

class TestViewsResourceFormGrant(test_django_oauth2.TestCase):
    
    def process(self, qs, data=None):
        if data is not None:
            return self.client.post('%s?%s' (reverse('resource'), urllib.urlencode(qs)), data)
        else:
            return self.client.get(reverse('resource'), qs)

    def test(self):
        user = self.getuser()
        access_token = AccessToken.objects.create(
            user=user,
            refreshable=True,
        )
        response = self.process({'oauth_token': access_token.token, })
        self.assertEquals(200, response.status_code)
        self.assertEquals('success', response.content)

if __name__ == '__main__':
    test_django_oauth2.main()
    