#-*- coding: utf-8 -*-
import urllib

import test_django_oauth2

from django.core.urlresolvers import reverse

from django_oauth2 import consts as appconsts
from django_oauth2.models import Client, Code

class TestViewTokenCodeIssue(test_django_oauth2.TestCase):
    
    def process(self, data):
        return self.client.post(
            reverse('django_oauth2_token'),
            data=urllib.urlencode(data),
            content_type='application/x-www-form-urlencoded'
        )

    def test_invalid_content_type(self):
        redirect_uri='http://www.google.fr'
        c = Client.objects.create(
            name='test',
            authorized_reponse_types=appconsts.RESPONSE_TYPES
        )
        code = Code.objects.create(
            client=c,
            redirect_uri=redirect_uri,
            user=self.getuser(),
        )
        data = {
            'grant_type': appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE,
            'client_id': c.key,
            'client_secret': c.secret,
            'code': code.key,
            'redirect_uri': redirect_uri,
        }
        self.assertTokenIssued(self.process(data))

if __name__ == '__main__':
    test_django_oauth2.main()
    