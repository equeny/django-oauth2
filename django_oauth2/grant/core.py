#-*- coding: utf-8 -*-

from django import forms
from django_oauth2.authentication.base import IBackend
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.sites.models import Site, RequestSite
from django.http import HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.http import urlquote, base36_to_int
from django.utils.translation import ugettext as _, ugettext_lazy
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache

from django.contrib.auth import forms as auth_form

from django_oauth2.views.authorize import authorization_grant_response,\
    authorization_deny_response

from django.contrib.auth.views import login
from django_oauth2.models import AuthorizationRequest, AccessRange

class Backend(IBackend):

    def authenticate(self, request, authorization_request):
        user = request.user
        if not user.is_authenticated():
            return handle_login_request(request, authorization_request_key=authorization_request.key)
        if True:
            return handle_scope_request(request, authorization_request_key=authorization_request.key)
        return authorization_grant()

STEP_LOGIN = 'login'
STEP_SCOPE = 'scope'

STEP_CHOICES = (
    (STEP_LOGIN, ugettext_lazy('Login')),
    (STEP_SCOPE, ugettext_lazy('Scope')),
    )

STATUS_GRANT = 'grant'
STATUS_DENY = 'deny'

STATUS_CHOICES = (
    (STATUS_GRANT, ugettext_lazy('Grant')),
    (STATUS_DENY, ugettext_lazy('Deny')),              
    )

class AuthenticationForm(auth_form.AuthenticationForm):
    step = forms.ChoiceField(widget=forms.HiddenInput, choices=STEP_CHOICES)
    authorization_request_key = forms.CharField(widget=forms.HiddenInput)

class ScopeForm(forms.Form):

    def __init__(self, authorization_request, *args, **kwargs):
        forms.Form.__init__(self, *args, **kwargs)
        self.fields.get('scope').choices = AccessRange.objects.filter(key__in=authorization_request.scope.split()).values_list('key', 'description')
        
    step = forms.ChoiceField(widget=forms.HiddenInput, choices=STEP_CHOICES)
    authorization_request_key = forms.CharField(widget=forms.HiddenInput)
    status = forms.ChoiceField(label=ugettext_lazy('Access'), widget=forms.RadioSelect, choices=STATUS_CHOICES)
    scope = forms.MultipleChoiceField(required=False, label=ugettext_lazy('Scope'), widget=forms.CheckboxSelectMultiple)

def handle(request):
    if request.method != 'POST':
        raise Http404(_('POST data expected'))
    step = request.POST.get('step')
    if step == STEP_LOGIN:
        return handle_login_response(request)
    elif step == STEP_SCOPE:
        return handle_scope_response(request)
    else: raise Http404(_('invalid step'))

def handle_login_request(request, authorization_request_key):
    data = {
        'step': STEP_LOGIN,
        'authorization_request_key': authorization_request_key,
        }
    form = AuthenticationForm(request, initial=data)
    return generate_login_page(request, form)

def handle_login_response(request):
    form = AuthenticationForm(data=request.POST)
    if form.is_valid():
        auth_login(request, form.get_user())
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()
        return handle_scope_request(request, form.cleaned_data.get('authorization_request_key'))
    return generate_login_page(request, form)

def generate_login_page(request, form):
    request.session.set_test_cookie()
    return render_to_response('django_oauth2/authentication/core/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))

def handle_scope_request(request, authorization_request_key):
    authorization_request = get_object_or_404(AuthorizationRequest, key=authorization_request_key)
    data = {
        'step': STEP_SCOPE,
        'authorization_request_key': authorization_request_key,
        'status': STATUS_GRANT,
        'scope': authorization_request.scope.split(),
        }
    form = ScopeForm(authorization_request, initial=data)
    return generate_scope_page(request, form, authorization_request)

def handle_scope_response(request):
    authorization_request = get_object_or_404(AuthorizationRequest, key=request.POST.get('authorization_request_key'))
    form = ScopeForm(authorization_request, data=request.POST)
    if form.is_valid():
        status = form.cleaned_data.get('status')
        scope = form.cleaned_data.get('scope')
        if status == STATUS_GRANT:
            return authorization_grant_response(authorization_request, scope)
        return authorization_deny_response(authorization_request)
    return generate_scope_page(request, form, authorization_request)

def generate_scope_page(request, form, authorization_request):
    return render_to_response('django_oauth2/authentication/core/scope.html', {
        'form': form,
    }, context_instance=RequestContext(request))

