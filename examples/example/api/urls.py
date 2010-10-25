#-*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import patterns, url

from piston.resource import Resource

from django_oauth2.piston import OAuth2Authentication

from example.api.handlers import DateHandler

date_handler = Resource(DateHandler, authentication=OAuth2Authentication())

urlpatterns = patterns('',
    url(r'^date/', date_handler, name='example-api-date'),
)
