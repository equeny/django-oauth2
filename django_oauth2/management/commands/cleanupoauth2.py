#-*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand

from django_oauth2.tools import generate_timestamp

class Command(NoArgsCommand):
    help = 'Can be run as a cronjob or directly to clean out old OAuth2 data from the database.'

    def handle_noargs(self, **options):
        from django.db import transaction
        from django_oauth2.models import AuthorizationRequest, AccessToken, Code
        now = generate_timestamp()
        AuthorizationRequest.objects.filter(expire__lt=now).delete()
        AccessToken.objects.filter(expire__lt=now).delete()
        Code.objects.filter(expire__lt=now).delete()
        transaction.commit_unless_managed()
