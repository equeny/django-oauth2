#-*- coding: utf-8 -*-
import urllib
import logging
import urlparse

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.http import absolute_http_url_re, HttpResponseRedirect, Http404,\
    HttpResponseBadRequest, HttpResponse

from django_oauth2.models import Client, Code, AccessToken, AuthorizationRequest, AccessRange
from django_oauth2 import settings as appsettings
from django_oauth2 import tools as oauth2_tools
from django_oauth2 import consts as appconsts
from django_oauth2 import OAuth2Error, MissRedirectUri
from django_oauth2.authentication import authenticate
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.utils import simplejson

from django_oauth2.tools import escape
from django import forms
from django_oauth2.tools import generate_timestamp

log = logging.getLogger(__name__)

ACCESS_ERRORS = {
    'invalid_request'   : ugettext_lazy('The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats the same parameter, uses more than one method for including an access token, or is otherwise malformed. The resource server MUST respond with the HTTP 400 (Bad Request) status code.'),
    'invalid_token'     : ugettext_lazy('The access token provided is invalid. Resource servers SHOULD use this error code when receiving an expired token which cannot be refreshed to indicate to the client that a new authorization is necessary. The resource server MUST respond with the HTTP 401 (Unauthorized) status code.'),
    'expired_token'     : ugettext_lazy('The access token provided has expired. Resource servers SHOULD only use this error code when the client is expected to be able to handle the response and request a new access token using the refresh token issued with the expired access token. The resource server MUST respond with the HTTP 401 (Unauthorized) status code.'),
    'insufficient_scope': ugettext_lazy('The request requires higher privileges than provided by the access token. The resource server SHOULD respond with the HTTP 403 (Forbidden) status code and MAY include the "scope" attribute with the scope necessary to access the protected resource.'),
}




class ResourceError(OAuth2Error):
    error = None

class InvalidRequest(ResourceError):
    error = 'invalid_request'

class InvalidToken(ResourceError):
    error = 'invalid_request'

class ExpiredToken(ResourceError):
    error = 'expired_token'

class InsufficientScope(ResourceError):
    error = 'insufficient_scope'

def getvalidator(grant_type):
    return {
        appconsts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE: AuthorizationCodeType,
        #appconsts.ACCESS_GRANT_TYPE_PASSWORD: PasswordType,
        #appconsts.ACCESS_GRANT_TYPE_ASSERTION: AssertionType,
        #appconsts.ACCESS_GRANT_TYPE_REFRESH_TOKEN: RefreshTokenType,
        #appconsts.ACCESS_GRANT_TYPE_NONE: NoneType,                               
    }.get(grant_type)

class AccessTokenProvider(object):

    def __init__(self, request):
        self.request = request

    def validate(self):
        query_token = self.analyze_query()
        header_token = self.analyze_header()
        body_token = self.analyze_body()
        # Check that only one
        
        self.oauth_token = query_token or header_token or body_token
        
        try: access_token = AccessToken.objects.get(token=self.oauth_token)
        except AccessToken.DoesNotExist:
            raise InvalidToken(_('The access token provided is invalid.'))
        
        if access_token.timestamp < generate_timestamp() - appsettings.ACCESS_TOKEN_EXPIRY:
            raise ExpiredToken(_('The access token provided has expired.'))

    def analyze_header(self):
        auth_header = self.request.META.get('HTTP_AUTHORIZATION')
        if auth_header is None:
            return
        if auth_header[:6] != 'OAuth ':
            return
        return auth_header[6:]

#    def _split_header(header):
#        """Turn Authorization: header into parameters."""
#        params = {}
#        parts = header.split(',')
#        for param in parts:
#            # Ignore realm parameter.
#            if param.find('realm') > -1:
#                continue
#            # Remove whitespace.
#            param = param.strip()
#            # Split key-value.
#            param_parts = param.split('=', 1)
#            # Remove quotes and unescape the value.
#            params[param_parts[0]] = urllib.unquote(param_parts[1].strip('\"'))
#        return params
#    _split_header = staticmethod(_split_header)

    def analyze_query(self):
        if self.request.GET.get('oauth_signature_method') is not None:
            raise
        token = self.request.GET.get('oauth_token')
        #if token is None:
        #    raise
        #TODO: check the last one
        #pass
        #parse_qsl((query_string or ''), True):
        return token

#    def _split_url_string(param_str):
#        """Turn URL string into parameters."""
#        parameters = cgi.parse_qs(param_str, keep_blank_values=False)
#        for k, v in parameters.iteritems():
#            parameters[k] = urllib.unquote(v[0])
#        return parameters
#    _split_url_string = staticmethod(_split_url_string)

    def analyze_body(self):
        class OAuthTokenForm(forms.Form):
            oauth_token = forms.CharField(required=True)
        form = OAuthTokenForm(self.request.POST)
        if form.is_valid():
            return form.cleaned_data['oauth_token']

    def deny(self, request, error):
        
        include_error = ( self.oauth_token is not None )
        
        auth_header = "OAuth realm='%s'" % appsettings.AUTHENTICATE_REALM
        data = {}
        if include_error:
            data = [
                ('error', error.error),
                ('error_description', u'%s' % error.message or u'%s' % ACCESS_ERRORS.get(error.error)),    # Handle ugettext_lazy files
                ('error_uri', '%s://%s%s' % (request.is_secure() and 'https' or 'http', Site.objects.get_current(), reverse('django_oauth2_authorize_error', kwargs={'error': error.error, }))),
                ('scope', self.scope),
                ]
        # Add the oauth parameters.
        for key, value in data:
            auth_header += ', %s="%s"' % (key, escape(str(v)))
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = auth_header
        return response
    
    def process(self):
        try: self.validate()
        except ResourceError, error:
            return self.deny(self.request, error)

class AccessGrantType(object):
    def __init__(self, request):
        self.request = request
    def validate(self):
        raise NotImplementedError
    def process(self):
        raise NotImplementedError
    def refreshable(self):
        pass

class AuthorizationCodeType(AccessGrantType):
    
    def __init__(self, request):
        super(AuthorizationCodeType).__init__(request)
        self.codekey = self.request.POST.get('code')
        self.redirect_uri = self.request.POST.get('redirect_uri')
        self.code = None

    def validate(self, client):
        if self.codekey is None:
            raise InvalidRequest(_('no code'))
        try: self.code = Code.objects.get(key=self.codekey)
        except Code.DoesNotExist:
            raise InvalidGrant(_('no such code: %(code)s') % {'code': self.codekey, })
        if self.redirect_uri is None:
            raise InvalidRequest(_('no redirect uri'))
        if not self.code.match_redirect_uri(self.redirect_uri):
            raise InvalidRequest(_("redirect_uri doesn't match"))
            
    def refreshable(self):
        return True

#class ResourceOwnerPasswordCredentials(AccessToken):
#    
#    def __init__(self, username, password, *args, **kwargs):
#        super(ResourceOwnerPasswordCredentials).__init__(*args, **kwargs)
#        self.username = username
#        self.password = password
#        
#class Assertion(AccessToken):
#    def __init__(self, assertion_type, assertion, *args, **kwargs):
#        super(Assertion).__init__(*args, **kwargs)
#        self.assertion_type = assertion_type
#        self.assertion = assertion
#
#class RefreshToken(AccessToken):
#    def __init__(self, refresh_token, *args, **kwargs):
#        super(RefreshToken).__init__(*args, **kwargs)
#        self.refresh_token = refresh_token

def handle_error(request, error):
    if not ACCESS_ERRORS.has_key(error):
        raise Http404(_("Access error %(error)s doesn't exist.") % {'error': error, })
    # Get the context
    context = {
        'error': error,
        'error_description': ACCESS_ERRORS.get(error)
        }
    # Render the form
    return render_to_response('django_oauth2/access_token/error.html', context_instance=RequestContext(request, context))

def handle_access_token(request):
    return AccessTokenProvider(request).process()
    
    