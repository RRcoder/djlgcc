from django.db import models
from django.conf import settings

class Sucursales(models.Model):
    nombre          = models.CharField(max_length=50)
    activo          = models.BooleanField()
    
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
    
    def __str__(self):
        return "id {} - {}".format(self.id, self.nombre)

class DatosUsuarios(models.Model):
    usuario  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="datos_usuario")
    sucursal = models.ForeignKey('Sucursales', on_delete=models.PROTECT)

class Comprobantes(models.Model):
    sucursal       = models.ForeignKey('Sucursales', on_delete=models.PROTECT)
    comprobante    = models.ForeignKey('TiposComprobante', on_delete=models.PROTECT)
    formulario     = models.CharField(max_length=1)
    punto_de_venta = models.IntegerField()
    activo         = models.BooleanField()

class TiposComprobante(models.Model):
    nombre = models.CharField(max_length=2)
    descripcion = models.CharField(max_length=30)

    def __str__(self):
        return "id {} - {} {}".format(self.id, self.nombre, self.descripcion)


