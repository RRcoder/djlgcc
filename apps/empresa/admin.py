from django.contrib import admin

from .models import *

@admin.register(Sucursales)
class SucursalesAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'activo']


@admin.register(DatosUsuarios)
class DatosUsuariosAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'sucursal']
    
@admin.register(Comprobantes)
class ComprobantesAdmin(admin.ModelAdmin):
    list_display = ['id', 'sucursal', 'comprobante', 'formulario', 'punto_de_venta', 'activo']


@admin.register(TiposComprobante)
class TiposComprobanteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion']

