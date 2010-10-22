#-*- coding: utf-8 -*-
from django.db import models

from django.utils.translation import ugettext_lazy as _


class SetField(models.TextField):

    default_validators = [validators.validate_comma_separated_integer_list]
    
    description = _('foobar')
    
    __metaclass__ = models.SubfieldBase
    
    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ' ')
        super(ChoiceSetField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, set):
            return value
        if getattr(value, '__iter__', False):
            return set(value)
        return set(value.split(self.token))
    
    def get_prep_value(self, value):
        return ''.join([''.join(l) for l in (value.north,
                value.east, value.south, value.west)])

    def formfield(self, **kwargs):
        # This is a fairly standard way to set up some defaults
        # while letting the caller override them.       
        defaults = {
            'error_messages': {
                'invalid': _(u'Enter only digits separated by commas.'),
            }
            ,
            'form_class': MyFormField,
            'widget': None,
        }
        defaults.update(kwargs)
        return super(HandField, self).formfield(**defaults)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def get_internal_type(self):
        return 'CharField'

class ChoiceSetField(models.TextField):
    
    description = _('foobar')
    
    __metaclass__ = models.SubfieldBase
    
    
    