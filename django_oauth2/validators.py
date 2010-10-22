import re
from django.core.validators import RegexValidator

comma_separated_int_list_re = re.compile('^[\d,]+$')
validate_comma_separated_integer_list = RegexValidator(comma_separated_int_list_re, _(u'Enter only digits separated by commas.'), 'invalid')
