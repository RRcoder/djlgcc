from django.contrib import admin

from .models import *

@admin.register(Provincias)
class ProvinciasAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'nombre']


@admin.register(TiposCliente)
class TiposClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descripcion']

