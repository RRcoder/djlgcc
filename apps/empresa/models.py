from django.db import models

class Sucursales(models.Model):
    nombre          = models.CharField(max_length=50)
    activo          = models.BooleanField()
    
    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
    
    def __str__(self):
        return "id {} - {}".format(self.id, self.nombre) 
