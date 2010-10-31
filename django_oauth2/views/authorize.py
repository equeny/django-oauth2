#-*- coding: utf-8 -*-
import urllib
import logging
import urlparse

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy
from django.http import absolute_http_url_re, HttpResponseRedirect, Http404,\
    HttpResponseBadRequest

from django_oauth2.models import Client, Code, AccessToken, AuthorizationRequest, AccessRange
from django_oauth2 import settings as appsettings
from django_oauth2 import tools as oauth2_tools
from django_oauth2 import consts as appconsts
from django_oauth2 import OAuth2Error, MissRedirectUri
from django_oauth2.authentication import authenticate
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

log = logging.getLogger(__name__)

AUTHORIZATION_ERRORS = {
    'invalid_request'          : ugettext_lazy('The request is missing a required parameter, includes an unsupported parameter or parameter value, or is otherwise malformed.'),
    'invalid_client'           : ugettext_lazy('The client identifier provided is invalid.'),
    'unauthorized_client'      : ugettext_lazy('The client is not authorized to use the requested response type.'),
    'redirect_uri_mismatch'    : ugettext_lazy('The redirection URI provided does not match a pre-registered value.'),
    'access_denied'            : ugettext_lazy('The end-user or authorization server denied the request.'),
    'unsupported_response_type': ugettext_lazy('The requested response type is not supported by the authorization server.'),
    'invalid_scope'            : ugettext_lazy('The requested scope is invalid, unknown, or malformed.'),
}

class AuthorizationError(OAuth2Error):
    error = None

class InvalidRequest(AuthorizationError):
    error = 'invalid_request'

class InvalidClient(AuthorizationError):
    error = 'invalid_client'

class UnauthorizedClient(AuthorizationError):
    error = 'unauthorized_client'
         
class RedirectUriMismatch(AuthorizationError):
    error = 'redirect_uri_mismatch'

class AccessDenied(AuthorizationError):
    error = 'access_denied'

class UnsupportedResponseType(AuthorizationError):
    error = 'unsupported_response_type'

class InvalidScope(AuthorizationError):
    error = 'invalid_scope'

class Authorization(object):

    def __init__(self, response_type, client_id, redirect_uri=None, scope=None, state=None):
        self.response_type = response_type
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        if self.scope is not None:
            self.scope = set(self.scope.split())
        self.state = state

    def validate(self):
        # Check client ID
        pass

    def get_redirect_uri(self, request=None):
        '''Get the redirect URI'''
        # Check if got a redirect URI
        if self.redirect_uri is None:
            # If no redirect URI, raise
            raise MissRedirectUri(_('No redirect_uri to send response.'))
        # If this is an absolute redirect URI, return it
        if absolute_http_url_re.match(self.redirect_uri):
            # Return the absolute URI
            return oauth2_tools.normalize_redirect_uri(self.redirect_uri)
        # The URL is not absolute, but check if starts with a slash to be able to build it with HTTP_REFERER
        #if not self.redirect_uri.startswith('/'):
        #    # Not an absolute 
        # If not absolute, 
        if not request:
            raise MissRedirectUri(_('Absolute redirect_uri required.'))
        http_referer = request.META.get('HTTP_REFERER')
        if http_referer is None or not absolute_http_url_re.match(http_referer) or not self.redirect_uri.startswith('/'):
            raise MissRedirectUri(_('Absolute redirect_uri required.'))
        split = list(urlparse.urlparse(http_referer))
        split[2] = self.redirect_uri    # Path
        split[3] = split[4] = split[5] = ''    # No parameters, query or fragment
        return urlparse.urlunparse(split)

    def deny(self, error, request=None):
        qs = {'error': error.error,
              'error_description': u'%s' % error.message or u'%s' % AUTHORIZATION_ERRORS.get(error.error),    # Handle ugettext_lazy files
              'error_uri': '%s://%s%s' % ('http', Site.objects.get_current(), reverse('django_oauth2_authorize_error', kwargs={'error': error.error, })),
              }
        if self.state is not None:
            qs['state'] = self.state
        return HttpResponseRedirect('%s?%s' % (self.get_redirect_uri(request), urllib.urlencode(qs, doseq=True)))
    
    def process(self):
        raise NotImplementedError

def handle_error(request, error):
    if not AUTHORIZATION_ERRORS.has_key(error):
        raise Http404(_("Authorization error %(error)s doesn't exist.") % {'error': error, })
    # Get the context
    context = {
        'error': error,
        'error_description': AUTHORIZATION_ERRORS.get(error)
        }
    # Render the form
    return render_to_response('django_oauth2/authorization/error.html', context_instance=RequestContext(request, context))

class Request(Authorization):
    
    def __init__(self, request):
        self.request = request
        super(Request, self).__init__(
            response_type = self.request.REQUEST.get('response_type'),
            client_id     = self.request.REQUEST.get('client_id'),
            redirect_uri  = self.request.REQUEST.get('redirect_uri'),
            scope         = self.request.REQUEST.get('scope'),
            state         = self.request.REQUEST.get('state'),
            )
        self.client = None

    def process(self):
        try: self.validate()
        except AuthorizationError, error:
            try: return self.deny(error, request=self.request)
            except MissRedirectUri, e:
                return HttpResponseBadRequest(e.message)
        authorization_request = AuthorizationRequest.objects.create(
            response_type=self.response_type,
            client=self.client,
            redirect_uri=self.redirect_uri,
            state=self.state,
            scope=self.scope
        )
        return authenticate(self.request, authorization_request)

    def validate(self):
        #import pdb
        #pdb.set_trace()
        #if self.request.META['CONTENT_TYPE'] != 'application/x-www-form-urlencoded':
        #    raise InvalidRequest()
        super(Request, self).validate()

        if self.client_id is None:
            raise InvalidRequest(_('No client_id'))
        try: self.client = Client.objects.get(key=self.client_id)
        except Client.DoesNotExist:
            raise InvalidClient(_("client_id %(client_id)s doesn't exist") % {'client_id': self.client_id, })
        # Redirect URI
        if self.redirect_uri is None:
            if self.client.redirect_uri is None:
                raise InvalidRequest(_('No redirect_uri provided or registered.'))
        elif self.client.redirect_uri and not self.client.match_redirect_uri(self.redirect_uri):
            self.redirect_uri = self.client.redirect_uri
            raise RedirectUriMismatch(_("Registered and provided redirect_uri doesn't match."))
        self.redirect_uri = self.redirect_uri or self.client.redirect_uri

        # Check no query / fragment etc

        # Check response type
        if self.response_type is None:
            raise InvalidRequest(_('Response type required'))
        if self.response_type not in appconsts.RESPONSE_TYPES:
            raise InvalidRequest(_('No such response type: %(response_type)s') % {'response_type': self.response_type, })
        if self.response_type not in appsettings.RESPONSE_TYPES:
            raise UnsupportedResponseType(_('Response type not supported by server: %(response_type)s') % {'response_type': self.response_type, })

        # Response type
        if not self.client.is_authorized_response_type(self.response_type):
            raise UnauthorizedClient(_('Response type %(response_type)s not allowed for client') % {'response_type': self.response_type, })
        
        if not absolute_http_url_re.match(self.redirect_uri):
            raise InvalidRequest(_('Absolute URI required for redirect_uri'))
        
        # Scope 
        if self.scope is not None:
            access_ranges = set(AccessRange.objects.filter(key__in=self.scope).values_list('key', flat=True))
            difference = access_ranges.symmetric_difference(self.scope)
            if len(difference) != 0:
                raise InvalidScope(_("Following access ranges doesn't exist: %(access_ranges)s") % {'access_ranges': ', '.join(difference), })

def handle_authorization_request(request):
    return Request(request).process()

class Response(Authorization):

    def __init__(self, authorization_request):
        self.client = authorization_request.client
        super(Response, self).__init__(
            response_type = authorization_request.response_type,
            client_id     = authorization_request.client_id,
            redirect_uri  = authorization_request.redirect_uri,
            scope         = authorization_request.scope,
            state         = authorization_request.state,
            )


class GrantResponse(Response):
    
    def process(self, user, scope):

        qs = {}
        frag = {}
        
        if self.response_type in [ appconsts.RESPONSE_TYPE_CODE, appconsts.RESPONSE_TYPE_CODE_AND_TOKEN ]:
            code = Code.objects.create(
                user=user, 
                client=self.client,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
            )
            qs['code'] = code.key
            
        if self.response_type in [ appconsts.RESPONSE_TYPE_TOKEN, appconsts.RESPONSE_TYPE_CODE_AND_TOKEN ]:
            
            access_token = AccessToken.objects.create(
                user=user,
                client=self.client,
                refreshable=False
            )
            
            frag['access_token'] = access_token.token
            
            # OPT
            frag['expires_in'] = appsettings.ACCESS_TOKEN_EXPIRY
            
            # OPT check if changed
            frag['scope'] = self.scope
    
        if self.state is not None:
            qs['state'] = self.state
        
        parts = list(urlparse.urlparse(self.redirect_uri))
        parts[4] = urllib.urlencode(qs, doseq=True)
        parts[5] = urllib.urlencode(frag, doseq=True)
        return HttpResponseRedirect(urlparse.urlunparse(parts))

def authorization_grant_response(authorization_request, user, scope):
    return GrantResponse(authorization_request).process(user, scope)

class DenyResponse(Response):
    
    def process(self, ):
        return self.deny(AccessDenied())
        
def authorization_deny_response(authorization_request):
    return DenyResponse(authorization_request).process()
    