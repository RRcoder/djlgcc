from django.contrib import admin

from .models import *

@admin.register(Provincias)
class ProvinciasAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'nombre']


@admin.register(TiposCliente)
class TiposClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descripcion']

@admin.register(Estadosped)
class EstadospedAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descripcion']


@admin.register(TiposIVA)
class TiposIVAAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'alicuota_iva']

@admin.register(Estadoscc)
class EstadosccAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descripcion']

@admin.register(TiposDocumento)
class TiposDocumentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'codigo', 'descripcion']

