#-*- coding: utf-8 -*-
import time

from django.db.models import PositiveIntegerField
from django_oauth2.tools import generate_timestamp

class TimestampField(PositiveIntegerField):

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.PositiveIntegerField'
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)

class CreationTimestampField(PositiveIntegerField):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('default', generate_timestamp)
        super(CreationTimestampField, self).__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return 'PositiveIntegerField'

    def south_field_triple(self):
        from south.modelsinspector import introspector
        field_class = 'django.db.models.fields.PositiveIntegerField'
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
