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
from django_oauth2 import consts as oauth2_consts
from django_oauth2 import OAuth2Error, MissRedirectUri
from django_oauth2.authentication import authenticate
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from django.utils import simplejson

log = logging.getLogger(__name__)

ACCESS_TOKEN_ERRORS = {
    'invalid_request'       : ugettext_lazy('The request is missing a required parameter, includes an unsupported parameter or parameter value, repeats a parameter, includes multiple credentials, utilizes more than one mechanism for authenticating the client, or is otherwise malformed.'),
    'invalid_client'        : ugettext_lazy('The client identifier provided is invalid, the client failed to authenticate, the client did not include its credentials, provided multiple client credentials, or used unsupported credentials type.'),
    'unauthorized_client'   : ugettext_lazy('The authenticated client is not authorized to use the access grant type provided.'),
    'invalid_grant'         : ugettext_lazy('The provided access grant is invalid, expired, or revoked (e.g. invalid assertion, expired authorization token, bad end-user password credentials, or mismatching authorization code and redirection URI).'),
    'unsupported_grant_type': ugettext_lazy('The access grant included - its type or another attribute - is not supported by the authorization server.'),
    'invalid_scope'         : ugettext_lazy('The requested scope is invalid, unknown, malformed, or exceeds the previously granted scope.'),
}

class AccessTokenError(OAuth2Error):
    error = None

class InvalidRequest(AccessTokenError):
    error = 'invalid_request'

class InvalidClient(AccessTokenError):
    error = 'invalid_client'

class UnauthorizedClient(AccessTokenError):
    error = 'unauthorized_client'
         
class InvalidGrant(AccessTokenError):
    error = 'invalid_grant'

class UnsupportedGrantType(AccessTokenError):
    error = 'unsupported_grant_type'

class InvalidScope(AccessTokenError):
    error = 'invalid_scope'


def getvalidator(grant_type):
    return {
        oauth2_consts.ACCESS_GRANT_TYPE_AUTHORIZATION_CODE: AuthorizationCodeType,
        #oauth2_consts.ACCESS_GRANT_TYPE_PASSWORD: PasswordType,
        #oauth2_consts.ACCESS_GRANT_TYPE_ASSERTION: AssertionType,
        #oauth2_consts.ACCESS_GRANT_TYPE_REFRESH_TOKEN: RefreshTokenType,
        #oauth2_consts.ACCESS_GRANT_TYPE_NONE: NoneType,                               
    }.get(grant_type)

class AccessTokenProvider(object):

    def __init__(self, request):
        self.request = request
        self.grant_type = self.request.POST.get('grant_type')
        self.client_id = self.request.POST.get('client_id')
        self.client_secret = self.request.POST.get('client_secret')
        self.scope = self.request.POST.get('scope')
        if self.scope is not None:
            self.scope = set(self.scope.split())
        self.validator = None

    def validate(self):
        if self.request.method != 'POST':
            raise InvalidRequest(_('POST requested'))
        if self.request.META['CONTENT_TYPE'] != 'application/x-www-form-urlencoded':
            raise InvalidRequest(_('invalid content type'))
        
        # Check response type
        if self.grant_type is None:
            raise InvalidRequest(_('grant type required'))
        if self.grant_type not in oauth2_consts.ACCESS_GRANT_TYPES:
            raise UnsupportedGrantType(_('No such grant type: %(grant_type)s') % {'grant_type': self.grant_type, })

        self.validator = getvalidator(self.grant_type)
        
        if self.client_id is None:
            raise InvalidRequest(_('No client_id'))
        try: self.client = Client.objects.get(key=self.client_id)
        except Client.DoesNotExist:
            raise InvalidClient(_("client_id %(client_id)s doesn't exist") % {'client_id': self.client_id, })
        # Redirect URI

    def deny(self, request, error):
        data = {'error': error.error,
              'error_description': u'%s' % error.message or u'%s' % ACCESS_TOKEN_ERRORS.get(error.error),    # Handle ugettext_lazy files
              'error_uri': '%s://%s%s' % (request.is_secure() and 'https' or 'http', Site.objects.get_current(), reverse('django_oauth2_authorize_error', kwargs={'error': error.error, })),
              }
        response = HttpResponseBadRequest(content=simplejson.dumps(data), content_type='application/json')
        response['Cache-Control'] = 'no-store'
        return response
    
    def process(self):
        try: self.validate()
        except AccessTokenError, error:
            return self.deny(self.request, error)
        access_token = AccessToken.objects.create(self.validator.refreshable())
        data = {
            'access_token': access_token.token,
            'expire_in': appsettings.ACCESS_TOKEN_EXPIRY,
            }
        if access_token.refresh_token:
            data['refresh_token'] = access_token.refresh_token
        if self.scope:
            data['scope'] = ' '.join(self.scope)
        response = HttpResponse(content=simplejson.dumps(data), content_type='application/json')
        response['Content-Type'] = 'no-store'
        return response

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
    if not ACCESS_TOKEN_ERRORS.has_key(error):
        raise Http404(_("Access token error %(error)s doesn't exist.") % {'error': error, })
    # Get the context
    context = {
        'error': error,
        'error_description': ACCESS_TOKEN_ERRORS.get(error)
        }
    # Render the form
    return render_to_response('django_oauth2/access_token/error.html', context_instance=RequestContext(request, context))

def handle_access_token(request):
    return AccessTokenProvider(request).process()
    
    