# -*- coding: utf-8 -*-
import os
import time
import codecs
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

version = '0.0.1'

folder = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(os.path.join(folder, 'PKG-INFO')):
    info = {
        'version': repr(version),
        'timestamp': int(time.time()),
    }
    fd = codecs.open(os.path.join(folder, 'django_oauth2', '__version__.py'), 'w', 'utf-8')
    fd.write("""#-*- coding: utf-8 -*-
version   = %(version)s
timestamp = %(timestamp)s
""" % info)
    
setup(
    name = 'django-oauth2',
    version = version,
    description = 'OAuth 2 application for Django.',
    url = 'http://code.google.com/p/django-oauth2/',
	download_url = 'http://pypi.python.org/pypi/django-oauth2/',
    license = '?',
    author = 'ShiningPanda',
    author_email = 'developers@shiningpanda.com',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = False,
    install_requires = [
        'Django>=1.2.3',
        'South==0.7.2',
    ],
    tests_require = [
        'coverage>=3.4',
        'Nosango>=0.1.0',               
    ],
    extras_require = {
        'PISTON': [
            'django-piston>=0.2.2',         
        ],            
    },
    setup_requires = [
        'collective.dist>=0.2.5',
    ],
    dependency_links = [
        'https://dev.shiningpanda.com/pypi/simple/nosango/'                  
    ],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Natural Language :: English',
    ],
    test_suite = 'nose.collector',
)