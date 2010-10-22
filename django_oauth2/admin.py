#-*- coding: utf-8 -*-
from django.contrib import admin

from django_oauth2.models import Client, AccessRange

# -----------------------------------------------------------------------------
# CLIENT
# -----------------------------------------------------------------------------
class ClientAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)

# -----------------------------------------------------------------------------
# ACCESS RANGE
# -----------------------------------------------------------------------------
class AccessRangeAdmin(admin.ModelAdmin):
    list_display = ('key', 'description')

admin.site.register(AccessRange, AccessRangeAdmin)
