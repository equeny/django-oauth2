#-*- coding: utf-8 -*-
import time
from django_oauth2 import consts
from django.http import HttpResponseRedirect, HttpResponse
import django

from django.utils import simplejson

class Client(object):
    pass

class Code(object):
    value = 1
    timestamp = 1
    client = Client()
    redirect_uri = 1

def authorize(request):
    
    # REQ
    response_type = request.REQUEST.get('response_type')
    
    # REQ
    client_id = request.REQUEST.get('client_id')
    
    # REQ unless set. If set and there, check that equals
    redirect_uri = request.REQUEST.get('redirect_uri')
    
    # OPT // space delimited
    scope = request.REQUEST.get('scope')
    
    # OPT
    state = request.REQUEST.get('state')
    
    
    code = Code()
    code.value = 1
    code.client = client_id
    code.timestamp = time.time()
    
    qs = {}
    frag = {}
    
    if response_type in [ consts.RESPONSE_TYPE_CODE, consts.RESPONSE_TYPE_CODE_AND_TOKEN ]:
        qs['code'] = code.value
        
    if response_type in [ consts.RESPONSE_TYPE_TOKEN, consts.RESPONSE_TYPE_CODE_AND_TOKEN]:
        frag['access_token'] = 1
        
        # OPT
        frag['expires_in'] = 3600
        
        # OPT check if changed
        frag['scope'] = scope

    qs['state'] = state
    
    
    return HttpResponseRedirect(redirect_uri)

def authorize_error(redirect_uri, error):
    pass

    qs = {'error':'',
          'error_description':'',
          'error_uri': '',
           'state': ''
          }

#   invalid_request
#         The request is missing a required parameter, includes an
#         unsupported parameter or parameter value, or is otherwise
#         malformed.
#
#   invalid_client
#         The client identifier provided is invalid.
#
#   unauthorized_client
#         The client is not authorized to use the requested response
#         type.
#
#   redirect_uri_mismatch
#         The redirection URI provided does not match a pre-registered
#         value.
#
#   access_denied
#         The end-user or authorization server denied the request.
#
#   unsupported_response_type
#         The requested response type is not supported by the
#         authorization server.
#
#   invalid_scope
#         The requested scope is invalid, unknown, or malformed.

def access_token(request):
    
    if request.method != 'POST':
        raise
    
    grant_type = request.POST.get('grant_type')
    
    client_id = request.POST.get('client_id')
    
    scope = request.POST.get('scope')
    
    
    if grant_type == consts.GRANT_TYPE_AUTHORIZATION_CODE:
        return access_token_authorization_code(request)
    elif grant_type == consts.GRANT_TYPE_PASSWORD:
        return access_token_password(request)
    elif grant_type == consts.GRANT_TYPE_ASSERTION:
        return access_token_assertion(request)
    elif grant_type == consts.GRANT_TYPE_REFRESH_TOKEN:
        return access_token_refresh_token(request)
    
def access_token_authorization_code(request):

    # REQ
    code = request.POST.get('code')
    
    # REQ
    redirect_uri = request.POST.get('redirect_uri')
    
    
    # Wired
    client_secret = request.POST.get('client_secret')
    
    # Validate the client credentials (if present) and ensure they match
    #  the authorization code
    
    # Verify that the authorization code and redirection URI are all
    #  valid and match its stored association.


def access_token_password(request):

    # REQ
    username = request.POST.get('username')

    # REQ
    password = request.POST.get('password')
    
    # Wired
    client_secret = request.POST.get('client_secret')
    

   #The authorization server MUST validate the client credentials (if
   #present) and end-user credentials and if valid issue an access token
   #response as described in Section 4.2.

def access_token_assertion(request):

    # REQ
    assertion_type = request.POST.get('assertion_type')

    # REQ
    assertion = request.POST.get('assertion')
    
    # There???
    client_secret = request.POST.get('client_secret')
    

   #The authorization server MUST validate the client credentials (if
   #present) and the assertion and if valid issues an access token
   #response as described in Section 4.2.  The authorization server
   #SHOULD NOT issue a refresh token (instead, require the client to use
   #the same or new assertion).

   #Authorization servers SHOULD issue access tokens with a limited
   #lifetime and require clients to refresh them by requesting a new
   #access token using the same assertion if it is still valid.
   #Otherwise the client MUST obtain a new valid assertion.


def access_token_refresh_token(request):
    
    # There???
    client_secret = request.POST.get('client_secret')
    
   #The authorization server MUST verify the client credentials (if
   #present), the validity of the refresh token, and that the resource
   #owner's authorization is still valid.  If the request is valid, the
   #authorization server issues an access token response as described in
   #Section 4.2.  The authorization server MAY issue a new refresh token.


def response_access_token(request):
    pass
    data = {
           'access_token': 1,
'expires_in': 1,
'refresh_token': 1,
'scope': 1,

            
            }
    
    content = simplejson.dumps(data, ensure_ascii=False, indent=4)
    
    response = HttpResponse(content, status=200, content_type='application/json')
    
    response['Cache-Control'] = 'no-store'

    return response

def response_access_token_error(request):

    data = {
           'error': 1,
'error_description': 1,
'error_uri': 1,

            
            }
    
    authorization = request.META.get('Authorization')  #] = request.META.get('HTTP_AUTHORIZATION', '')
    
    status = authorization and 401 or 400
    
    content = simplejson.dumps(data, ensure_ascii=False, indent=4)
    
    response = HttpResponse(content, status=status, content_type='application/json')
    
    response['Cache-Control'] = 'no-store'

    return response
#
#   invalid_request
#         The request is missing a required parameter, includes an
#         unsupported parameter or parameter value, repeats a parameter,
#         includes multiple credentials, utilizes more than one mechanism
#         for authenticating the client, or is otherwise malformed.
#
#   invalid_client
#         The client identifier provided is invalid, the client failed to
#         authenticate, the client did not include its credentials,
#         provided multiple client credentials, or used unsupported
#         credentials type.
#
#   unauthorized_client
#         The authenticated client is not authorized to use the access
#         grant type provided.
#
#   invalid_grant
#         The provided access grant is invalid, expired, or revoked (e.g.
#         invalid assertion, expired authorization token, bad end-user
#         password credentials, or mismatching authorization code and
#         redirection URI).
#
#   unsupported_grant_type
#         The access grant included - its type or another attribute - is
#         not supported by the authorization server.
#
#   invalid_scope
#         The requested scope is invalid, unknown, malformed, or exceeds
#         the previously granted scope.


def access(request):
    auth_header = request.META.get('HTTP_AUTHORIZATION')
    if auth_header is not None:
        return access_header(request, auth_header)
    oauth_token = request.GET.get('oauth_token')
    if oauth_token is not None:
        return access_query(request, oauth_token)
    
def access_header(request, auth_header):
    pass
    access_token = 1


def access_query(request, value):
    pass


def access_form(request):
    pass
    # No oauth_signature_method

#   When including the access token in the HTTP request entity-body, the
#   client adds the access token to the request body using the
#   "oauth_token" parameter.  The client can use this method only if the
#   following REQUIRED conditions are met:
#
#   o  The entity-body is single-part.
#
#   o  The entity-body follows the encoding requirements of the
#      "application/x-www-form-urlencoded" content-type as defined by
#      [W3C.REC-html401-19991224].
#
#   o  The HTTP request entity-header includes the "Content-Type" header
#      field set to "application/x-www-form-urlencoded".
#
#   o  The HTTP request method is "POST", "PUT", or "DELETE".

def access_error(request):
    
    response = HttpResponse(status=401)
    response['WWW-Authenticate'] = ''
    
    
#   invalid_request
#         The request is missing a required parameter, includes an
#         unsupported parameter or parameter value, repeats the same
#         parameter, uses more than one method for including an access
#         token, or is otherwise malformed.  The resource server MUST
#         respond with the HTTP 400 (Bad Request) status code.
#
#   invalid_token
#         The access token provided is invalid.  Resource servers SHOULD
#         use this error code when receiving an expired token which
#         cannot be refreshed to indicate to the client that a new
#         authorization is necessary.  The resource server MUST respond
#         with the HTTP 401 (Unauthorized) status code.
#
#   expired_token
#         The access token provided has expired.  Resource servers SHOULD
#         only use this error code when the client is expected to be able
#         to handle the response and request a new access token using the
#         refresh token issued with the expired access token.  The
#         resource server MUST respond with the HTTP 401 (Unauthorized)
#         status code.
#
#   insufficient_scope
#         The request requires higher privileges than provided by the
#         access token.  The resource server SHOULD respond with the HTTP
#         403 (Forbidden) status code and MAY include the "scope"
#         attribute with the scope necessary to access the protected
#         resource.

