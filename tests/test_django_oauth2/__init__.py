#-*- coding: utf-8 -*-
import os
import sys
import nose
import urlparse

import nosango.cases

import django.test.client
from django.core.urlresolvers import reverse
from django_oauth2.authorize import authorization_grant_response

# Absolute folder of this file
FOLDER = os.path.dirname(os.path.abspath(__file__))

class TestCase(nosango.cases.TestCase):
    '''Super class of test'''

    base = FOLDER

    def setUp(self):
        '''Set up for the test case'''
        # Call super
        super(TestCase, self).setUp()
        # Create a client
        self.client = django.test.client.Client()
    
    def assertAuthorizeError(self, data, error, error_description=None, error_uri=None, redirect_uri=None):
        response = self.client.get(reverse('django_oauth2_authorize'), data=data)
        self.assertEquals(302, response.status_code)
        self.assertTrue(response.has_header('Location'))
        location = response['Location']
        location_parts = urlparse.urlparse(location)
        location_qs = urlparse.parse_qs(location_parts.query)
        redirect_uri_parts = urlparse.urlparse(redirect_uri or data['redirect_uri'])
        self.assertEquals(redirect_uri_parts.scheme, location_parts.scheme)
        self.assertEquals(redirect_uri_parts.netloc, location_parts.netloc)
        self.assertEquals(redirect_uri_parts.path, location_parts.path)
        self.assertEquals('', location_parts.params)
        self.assertEquals('', location_parts.fragment)
        for key in location_qs.keys():
            self.assertTrue(key in ['error', 'error_description', 'error_uri', 'state'])
        self.assertTrue(location_qs.has_key('error'))
        self.assertEquals([error, ], location_qs['error'])
        if data.has_key('state'):
            self.assertTrue(location_qs.has_key('state'))
            self.assertEquals([data['state'], ], location_qs['state'])
        else: self.assertFalse(location_qs.has_key('state'))
        if error_description is not None:
            self.assertTrue(location_qs.has_key('error_description'))
            self.assertEquals([error_description, ], location_qs['error_description'])
        if error_uri is not None:
            self.assertTrue(location_qs.has_key('error_uri'))
            self.assertEquals([error_description, ], location_qs['error_uri'])
    
    def assertGrantCode(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
    def assertGrantToken(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
    def assertGrantCodeAndToken(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
     
def main():
    '''Run test'''
    # Get line
    argv = list(sys.argv)
    # Add configuration
    argv.extend(['-c', os.path.join(FOLDER, 'setup.cfg'), ])
    # Run test
    nose.runmodule(argv=argv)
