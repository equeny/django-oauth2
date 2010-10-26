#-*- coding: utf-8 -*-
import os
import sys
import nose
import urlparse

import nosango.cases

import django.test.client
from django.utils import simplejson
from django.core.urlresolvers import reverse
from django_oauth2.views.authorize import authorization_grant_response

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
        location_parts = self.assertRedirectUri(response, redirect_uri)
        location_qs = urlparse.parse_qs(location_parts.query)
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
    
    def assertRedirectUri(self, response, redirect_uri): #, qs='', frag=''):
        self.assertTrue(response.has_header('Location'))
        location = response['Location']
        location_parts = urlparse.urlparse(location)
        redirect_uri_parts = urlparse.urlparse(redirect_uri)
        self.assertEquals('', redirect_uri_parts.params) # Check test reference
        self.assertEquals('', redirect_uri_parts.query) # Check test reference
        self.assertEquals('', redirect_uri_parts.fragment) # Check test reference
        self.assertEquals(redirect_uri_parts.scheme, location_parts.scheme)
        self.assertEquals(redirect_uri_parts.netloc, location_parts.netloc)
        self.assertEquals(redirect_uri_parts.path, location_parts.path)
        self.assertEquals('', location_parts.params)
        #if isinstance(qs, dict):
        #    location_qs = urlparse.parse_qs(location_parts.query)
        #    self.assertEquals(self.dict_to_doseq(qs), location_qs)
        #else: self.assertEquals(qs, location_parts.query)
        #if isinstance(frag, dict):
        #    location_frag = urlparse.parse_qs(location_parts.fragment)
        #    self.assertEquals(self.dict_to_doseq(frag), location_frag)
        #else: self.assertEquals(frag, location_parts.fragment)
        return location_parts
    
    #def dict_to_doseq(self, data):
    #    doseq = {}
    #    for key in data.keys():
    #        doseq[key] = [data[key], ]
    #    return doseq
    
    def assertAuthorizeGrantCode(self, response, redirect_uri, code):
        self.assertEquals(302, response.status_code)
        location_parts = self.assertRedirectUri(response, redirect_uri)
        self.assertEquals('', location_parts.fragment)
        location_qs = urlparse.parse_qs(location_parts.query)
        self.assertTrue(location_qs.has_key('code'))
        self.assertEquals([code, ], location_qs['code'])
    
    def assertAuthorizeGrantToken(self, response, redirect_uri, access_token):
        self.assertEquals(302, response.status_code)
        location_parts = self.assertRedirectUri(response, redirect_uri)
        self.assertEquals('', location_parts.query)
        location_frag = urlparse.parse_qs(location_parts.fragment)
        self.assertTrue(location_frag.has_key('access_token'))
        self.assertEquals([access_token, ], location_frag['access_token'])
    
    def assertAuthorizeGrantCodeToken(self, response, redirect_uri, code, access_token):
        self.assertEquals(302, response.status_code)
        location_parts = self.assertRedirectUri(response, redirect_uri)
        location_qs = urlparse.parse_qs(location_parts.query)
        self.assertTrue(location_qs.has_key('code'))
        self.assertEquals([code, ], location_qs['code'])
        location_frag = urlparse.parse_qs(location_parts.fragment)
        self.assertTrue(location_frag.has_key('access_token'))
        self.assertEquals([access_token, ], location_frag['access_token'])

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
     
    def assertTokenIssued(self, response):
        self.assertEquals(200, response.status_code)
        self.assertEquals('application/json', response['Content-Type'])
        self.assertEquals('no-store', response['Cache-Control'])
        data = simplejson.loads(response.content)
        self.assertTrue(data.has_key('access_token'))
#        if error_description is not None:
#            self.assertTrue(data.has_key('error_description'))
#            self.assertEquals(error_description, data['error_description'])
#        if error_uri is not None:
#            self.assertTrue(data.has_key('error_uri'))
#            self.assertEquals(error_description, data['error_uri'])
        
     
def main():
    '''Run test'''
    # Get line
    argv = list(sys.argv)
    # Add configuration
    argv.extend([
        '--verbosity=2',
        '--exe',
        '--nocapture',
        '--with-nosango',
    ])
    # Run test
    nose.runmodule(argv=argv)
