#-*- coding: utf-8 -*-
import os
import sys
import nose
import urlparse

import nosango.cases

import django.test.client
from django.utils import simplejson
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
    
    def assertAuthorizeError(self, response, redirect_uri, error, error_description=None, error_uri=None, state=None):
        self.assertEquals(302, response.status_code)
        self.assertTrue(response.has_header('Location'))
        location = response['Location']
        location_parts = urlparse.urlparse(location)
        location_qs = urlparse.parse_qs(location_parts.query)
        redirect_uri_parts = urlparse.urlparse(redirect_uri)
        self.assertEquals(redirect_uri_parts.scheme, location_parts.scheme)
        self.assertEquals(redirect_uri_parts.netloc, location_parts.netloc)
        self.assertEquals(redirect_uri_parts.path, location_parts.path)
        self.assertEquals('', location_parts.params)
        self.assertEquals('', location_parts.fragment)
        for key in location_qs.keys():
            self.assertTrue(key in ['error', 'error_description', 'error_uri', 'state'])
        self.assertTrue(location_qs.has_key('error'))
        self.assertEquals([error, ], location_qs['error'])
        if state is not None:
            self.assertTrue(location_qs.has_key('state'))
            self.assertEquals([state, ], location_qs['state'])
        else: self.assertFalse(location_qs.has_key('state'))
        if error_description is not None:
            self.assertTrue(location_qs.has_key('error_description'))
            self.assertEquals([error_description, ], location_qs['error_description'])
        if error_uri is not None:
            self.assertTrue(location_qs.has_key('error_uri'))
            self.assertEquals([error_description, ], location_qs['error_uri'])
    
    def assertTokenError(self, response, error, error_description=None, error_uri=None, status_code=400):
        self.assertEquals(status_code, response.status_code)
        self.assertEquals('application/json', response['Content-Type'])
        self.assertEquals('no-store', response['Cache-Control'])
        data = simplejson.loads(response.content)
        self.assertTrue(data.has_key('error'))
        if error_description is not None:
            self.assertTrue(data.has_key('error_description'))
            self.assertEquals(error_description, data['error_description'])
        if error_uri is not None:
            self.assertTrue(data.has_key('error_uri'))
            self.assertEquals(error_description, data['error_uri'])
    
    def assertGrantCode(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
    def assertGrantToken(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
    def assertGrantCodeAndToken(self, authorization_request):
        response = authorization_grant_response(authorization_request, 'foo')
        self.assertEquals(302, response.status_code)
    
     
    def assertFoo(self, response):
        pass
     
def main():
    '''Run test'''
    # Get line
    argv = list(sys.argv)
    # Add configuration
    argv.extend(['-c', os.path.join(FOLDER, 'setup.cfg'), ])
    # Run test
    nose.runmodule(argv=argv)
