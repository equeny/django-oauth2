#-*- coding: utf-8 -*-
import time
import urllib
import urlparse
from random import choice

def generate_unique_key(klass, key_length, key_field='key'):
    while True:
        key_value = generate_key(length=key_length)
        if not klass.objects.filter(**{key_field: key_value, }).count():
            return key_value

def generate_key(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'):
    '''Generates a random password with the given length and given allowed_chars'''
    return ''.join([choice(allowed_chars) for i in range(length)])

def normalize_redirect_uri(uri):
    parts = urlparse.urlsplit(uri)
    scheme, netloc, path = parts[:3]
    if scheme == 'http' and netloc[-3:] == ':80':
        netloc = netloc[:-3]
    elif scheme == 'https' and netloc[-4:] == ':443':
        netloc = netloc[:-4]
    if path == '/': path = ''
    return '%s://%s%s' % (scheme, netloc, path)

def escape(s):
    return urllib.quote(s, safe='~')

def generate_timestamp(future=0):
    return int(time.time()) + future
