from django.contrib import admin

from .models import *

@admin.register(Sucursales)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'activo']
