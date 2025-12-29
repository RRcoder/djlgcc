from django.db import models
from django.conf import settings


class TiposCliente(models.Model):
    codigo                 = models.CharField(max_length=1)
    descripcion            = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

class Provincias(models.Model):
    codigo        = models.CharField(max_length=1)
    nombre        = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Clientes(models.Model):
    nombre                 = models.CharField(max_length=200)
    domicilio_calle        = models.CharField(max_length=200)
    domicilio_numero       = models.CharField(max_length=10)
    domicilio_piso         = models.CharField(max_length=10, null=True, blank=True)
    domicilio_departamento = models.CharField(max_length=10, null=True, blank=True) 
    codigo_postal          = models.CharField(max_length=10, null=True, blank=True) 
    localidad              = models.CharField(max_length=200, null=True, blank=True)
    provincia              = models.ForeignKey('Provincias', on_delete=models.PROTECT) 
    telefono_fijo          = models.CharField(max_length=50, null=True, blank=True)
    telefono_celular       = models.CharField(max_length=10, null=True, blank=True)
    email                  = models.EmailField(blank=True, null=True) 
    tipo_documento         = models.ForeignKey('TiposDocumento', on_delete=models.PROTECT) 
    cuit                   = models.BigIntegerField() 
    tipo                   = models.ForeignKey('TiposCliente', on_delete=models.PROTECT) 
    sucursal               = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT, blank=True, null=True)
    activo                 = models.BooleanField() 
    updated                = models.DateTimeField(auto_now=True)
    created                = models.DateTimeField(auto_now_add=True)
    
    estadoctacte     = models.ForeignKey('Estadoscc', on_delete=models.PROTECT, null=True, blank=True)
    tolerancia = models.IntegerField(null=True, blank= True)
    credito    = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  
    febaja     = models.DateField(null=True, blank=True) 
    motivobaja = models.CharField(max_length=250, null=True, blank=True)

    def get_domicilio(self):
        piso_dpto=''
        if self.domicilio_piso is not None:
            piso_dpto+= " Piso {}".format(self.domicilio_piso)
        
        if self.domicilio_departamento is not None:
            piso_dpto+= " Dpto: {}".format(self.domicilio_departamento)

        return "{} {} {}".format(self.domicilio_calle, self.domicilio_numero, piso_dpto)

    def get_documento(self):
        #if self.tipo.codigo=='F':
            #return "DNI: {}".format(self.cuit)

        #if self.tipo.codigo=='J':
            #return "CUIT: {}".format(self.cuit)
        return "{}: {}".format(self.tipo_documento.codigo, self.cuit)

    def get_localidad_provincia(self):
        rta=''
        if self.localidad is not None:
            rta+= self.localidad
        
        if self.provincia is not None:
            if len(rta)>0:
                rta+= " - " + self.provincia.nombre
            else:
                rta+= self.provincia.nombre

        return rta

    def __str__(self):
        return "({}) {}".format(self.id, self.nombre)

class Remitos(models.Model):
    fecha          = models.DateField() 
    punto_de_venta = models.IntegerField()
    numero         = models.IntegerField()
    cliente        = models.ForeignKey('Clientes', on_delete=models.PROTECT)
    bultos         = models.IntegerField(null=True, blank=True)
    pesoaprox      = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) 
    valoraprox     = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True) 
    impreso        = models.BooleanField(null=True, blank=True)
    sucursal       = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT)
    usuario        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    created        = models.DateTimeField(auto_now_add=True)
    #lista          = models. 
    #estado         = models.
    #condvta        = models. 
    
    def __str__(self):
        return "RTO {:05d}-{:08d}".format(self.punto_de_venta, self.numero)

class RemitosDet(models.Model):
    remito           = models.ForeignKey('Remitos', on_delete=models.PROTECT, related_name='detalles')
    codigo           = models.CharField(max_length=10, null=True, blank=True)
    descripcion      = models.CharField(max_length=60)
    importe_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    costo            = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    cantidad         = models.DecimalField(max_digits=7, decimal_places=2) 
    alicuota_iva     = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    
    dtounit          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    importe_iva      = models.DecimalField(max_digits=12, decimal_places=2, null= True, blank=True)
    #nped      | int(11)       | YES  |     | NULL    |                |
    #codrep          | varchar(20)   | YES  |     | NULL    |                |

    @property
    def total(self):
        """Calcula el total por ítem, con o sin descuento"""
        precio_unitario = self.importe_unitario or 0
        cantidad = self.cantidad or 0
        return precio_unitario * cantidad



class PedidosTmp(models.Model):
    fecha        = models.DateField(null=True, blank=True)
    proceso      = models.ForeignKey('Procesos', on_delete=models.PROTECT)
    cliente      = models.ForeignKey('Clientes', on_delete=models.PROTECT,null=True, blank=True)
    sucursal     = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT, null=True, blank=True)
    codigo       = models.CharField(max_length=10, null=True, blank=True)
    descripcion  = models.CharField(max_length=100, null=True, blank=True)
    precio       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    costo        = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    cantidad     = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    alicuota_iva = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    
    rm_realizado = models.IntegerField(null=True, blank=True) 
    edit_id      = models.IntegerField(null=True, blank=True) # este campo sirve para guardar el id del pedido en el caso de edicion de un pedido.
    updated      = models.DateTimeField(auto_now=True)
    created      = models.DateTimeField(auto_now_add=True)

class Procesos(models.Model):
    nombre      = models.CharField(max_length=20, null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)


class Pedidos(models.Model):
    fecha        = models.DateField(null=True, blank=True)
    cliente      = models.ForeignKey('Clientes', on_delete=models.PROTECT,null=True, blank=True)
    sucursal     = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT, null=True, blank=True)
    rm_realizado = models.IntegerField(null=True, blank=True) 
    estado       = models.ForeignKey('Estadosped', on_delete=models.PROTECT, null=True, blank=True)
    rm_asociado  = models.ForeignKey('Remitos', on_delete=models.PROTECT,null=True, blank=True)
    usuario      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    updated      = models.DateTimeField(auto_now=True)
    created      = models.DateTimeField(auto_now_add=True)

class PedidosDet(models.Model):
    pedido           = models.ForeignKey('Pedidos', on_delete=models.CASCADE, related_name='detalles')
    codigo           = models.CharField(max_length=10, null=True, blank=True)
    descripcion      = models.CharField(max_length=100, null=True, blank=True)
    importe_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    costo            = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    cantidad         = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    




class Estadosped(models.Model):
    codigo                 = models.CharField(max_length=1)
    descripcion            = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"





class TiposIVA(models.Model):
    codigo      = models.CharField(max_length=10)
    alicuota_iva= models.DecimalField(max_digits=5, decimal_places=2)    

class ListaPrecios(models.Model):
    codigo      = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)
    precio      = models.DecimalField(max_digits=12, decimal_places=2)    
    costo       = models.DecimalField(max_digits=12, decimal_places=2)    
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ("{} - {}".format(self.codigo, self.descripcion))
# en vez de hacer en otra tabla se metio los campos en la clientes
#class Ctacte(models.Model):
    #cliente    = models.OnetoOneFeild('Clientes', on_delete=models.PROTECT)
    #estado     = models.ForeignKey('Clientes', on_delete=models.PROTECT)
    #moroso     =
    #tolerancia = models.IntegerField(null=True, blank= True)
    #credito    = models.DecimalField(max_digits=12, decimal_places=2)  
    #febaja     = models.DateField(null=True, blank=True) 
    #motivobaja = models.CharField(max_length=250, null=True, blank=True)
    #updated    = models.DateTimeField(auto_now=True)
    #created    = models.DateTimeField(auto_now_add=True)

class Estadoscc(models.Model):
    codigo                 = models.CharField(max_length=1)
    descripcion            = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.codigo} - {self.descripcion}"

# la pregunta seria porque si apunto al id del cliente grabo el tipo de doc y el nro. 
# Simple porque la gente usuario de software a VECES EDITA los campos del cliente, y eso arruinaria todos
# los movimientos grabados, sin embargo ya estan registrados.
class Movimientos(models.Model):
    cliente          = models.ForeignKey('Clientes', on_delete=models.PROTECT,null=True, blank=True)
    tipo_documento   = models.ForeignKey('TiposDocumento', on_delete=models.PROTECT,null=True, blank=True)
    numero_documento = models.BigIntegerField() 
    fecomp           = models.DateField()
    formulario       = models.CharField(max_length=10, null=True, blank=True)
    tipocomp         = models.IntegerField()  
    sucucomp         = models.IntegerField() 
    nrocomp          = models.IntegerField() 
    importe          = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)  
    importe_iva      = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    importe_total    = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    alicuota_iva     = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    
    updated          = models.DateTimeField(auto_now=True)
    created          = models.DateTimeField(auto_now_add=True)


class TiposDocumento(models.Model):
    codigo      = models.CharField(max_length=4, null=True, blank=True)
    descripcion = models.CharField(max_length=50, null=True, blank=True)
    


s="""
campos en el remito

cabecera

RM
form
sucu
nro
fecha


nombre Empresa
sucursal
direccion
cp localidad - provincia
tel
email

cuit 
IIBB
Inicio act


mysql> describe cctacte;
+--------------+---------------+------+-----+---------+-------+
| Field        | Type          | Null | Key | Default | Extra |
+--------------+---------------+------+-----+---------+-------+
| cliente      | int(11)       | YES  |     | NULL    |       |
| nrocta       | int(11)       | YES  | MUL | NULL    |       |
| sucursal     | int(11)       | YES  |     | NULL    |       |
| categ        | int(11)       | YES  |     | NULL    |       |
| estado       | varchar(1)    | YES  |     | NULL    |       |
| moroso       | varchar(1)    | YES  |     | NULL    |       |
| tolerancia   | int(11)       | YES  |     | NULL    |       |
| credito      | decimal(12,2) | YES  |     | NULL    |       |
| saldo        | decimal(12,2) | YES  |     | NULL    |       |
| fealta       | date          | YES  |     | NULL    |       |
| febaja       | date          | YES  |     | NULL    |       |
| fecredito    | date          | YES  |     | NULL    |       |
| feultoper    | date          | YES  |     | NULL    |       |
| feultpago    | date          | YES  |     | NULL    |       |
| condvta      | int(11)       | YES  |     | NULL    |       |
| motivobaja   | varchar(20)   | YES  |     | NULL    |       |
| concep       | int(11)       | YES  |     | NULL    |       |
| intcont      | int(11)       | YES  |     | NULL    |       |
| notificacion | char(1)       | YES  |     | N       |       |
| fe_arch      | date          | YES  |     | NULL    |       |
| envia_resu   | char(1)       | YES  |     | NULL    |       |
+--------------+---------------+------+-----+---------+-------+
21 rows in set (0.01 sec)

mysql> select * from cctacte limit 1000,1;
+---------+--------+----------+-------+--------+--------+------------+---------+--------+------------+------------+------------+------------+------------+---------+----------------------+--------+---------+--------------+------------+------------+
| cliente | nrocta | sucursal | categ | estado | moroso | tolerancia | credito | saldo  | fealta     | febaja     | fecredito  | feultoper  | feultpago  | condvta | motivobaja           | concep | intcont | notificacion | fe_arch    | envia_resu |
+---------+--------+----------+-------+--------+--------+------------+---------+--------+------------+------------+------------+------------+------------+---------+----------------------+--------+---------+--------------+------------+------------+
|    9488 |      2 |        0 |     4 | B      |        |         30 | 1000.00 | 948.88 | 2000-07-12 | 2011-09-12 | 2000-07-12 | 2009-06-19 | 2009-05-12 |       0 |                      |      0 |       0 | N            | 2016-10-16 | NULL       |
+---------+--------+----------+-------+--------+--------+------------+---------+--------+------------+------------+------------+------------+------------+---------+----------------------+--------+---------+--------------+------------+------------+
1 row in set (0.08 sec)
mysql> select * from cctacte where cliente=7721;
+---------+--------+----------+-------+--------+--------+------------+-------------+----------+------------+------------+------------+------------+------------+---------+------------+--------+---------+--------------+------------+------------+
| cliente | nrocta | sucursal | categ | estado | moroso | tolerancia | credito     | saldo    | fealta     | febaja     | fecredito  | feultoper  | feultpago  | condvta | motivobaja | concep | intcont | notificacion | fe_arch    | envia_resu |
+---------+--------+----------+-------+--------+--------+------------+-------------+----------+------------+------------+------------+------------+------------+---------+------------+--------+---------+--------------+------------+------------+
|    7721 |      2 |        0 |     1 | A      |        |          0 | 45000000.00 | 59888.67 | 1999-05-17 | 2017-07-14 | 1999-05-17 | 2009-06-22 | 2009-05-26 |       2 |            |      0 |       0 | N            | 2016-10-16 | S          |
+---------+--------+----------+-------+--------+--------+------------+-------------+----------+------------+------------+------------+------------+------------+---------+------------+--------+---------+--------------+------------+------------+

















"""
