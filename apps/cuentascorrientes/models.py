from django.db import models


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
        if self.tipo.codigo=='F':
            return "DNI: {}".format(self.cuit)

        if self.tipo.codigo=='J':
            return "CUIT: {}".format(self.cuit)

    def __str__(self):
        return "({}) {}".format(self.id, self.nombre)

class Remitos(models.Model):
    fecha          = models.DateField() 
    punto_de_venta = models.IntegerField()
    numero         = models.IntegerField()
    cliente        = models.ForeignKey('Clientes', on_delete=models.PROTECT)
    #lista          = models. 
    bultos         = models.IntegerField()
    pesoaprox      = models.DecimalField(max_digits=6, decimal_places=2) 
    valoraprox     = models.DecimalField(max_digits=6, decimal_places=2) 
    impreso        = models.BooleanField()
    #estado         = models.
    sucursal       = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT)
    #condvta        = models. 
    #responsable    =
    #transporte     =

class RemitosDet(models.Model):
    remito           = models.ForeignKey('Remitos', on_delete=models.PROTECT)
    #codrep          | varchar(20)   | YES  |     | NULL    |                |
    descripcion      = models.CharField(max_length=60)
    cantidad         = models.DecimalField(max_digits=7, decimal_places=2) 
    importe_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    dtounit          = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    importe_iva      = models.DecimalField(max_digits=12, decimal_places=2, null= True, blank=True)
    #nped      | int(11)       | YES  |     | NULL    |                |


class Pedidos(models.Model):
    fecha          = models.DateField(null=True, blank=True)
    proceso        = models.ForeignKey('Procesos', on_delete=models.PROTECT)
    cliente        = models.ForeignKey('Clientes', on_delete=models.PROTECT,null=True, blank=True)
    sucursal       = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT, null=True, blank=True)
    codigo         = models.CharField(max_length=10, null=True, blank=True)
    descripcion    = models.CharField(max_length=100, null=True, blank=True)
    precio         = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    costo          = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    cantidad       = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)    
    alicuota_iva   = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)    
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)

class Procesos(models.Model):
    nombre      = models.CharField(max_length=20, null=True, blank=True)
    updated     = models.DateTimeField(auto_now=True)
    created     = models.DateTimeField(auto_now_add=True)


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






s="""
describe remito21;
+------------+---------------+------+-----+---------+----------------+
| Field      | Type          | Null | Key | Default | Extra          |
+------------+---------------+------+-----+---------+----------------+
| fecha      | date          | YES  |     | NULL    |                |
| nroint     | int(11)       | NO   | PRI | NULL    | auto_increment |
| sucuremi   | int(11)       | YES  |     | NULL    |                |
| nroremi    | int(11)       | YES  |     | NULL    |                |
| talonario  | int(11)       | YES  |     | NULL    |                |
| cliente    | int(11)       | YES  |     | NULL    |                |
| nrocta     | int(11)       | YES  |     | NULL    |                |
| tipoped    | varchar(1)    | YES  |     | NULL    |                |
| ocpra      | varchar(10)   | YES  |     | NULL    |                |
| condvta    | int(11)       | YES  |     | NULL    |                |
| lista      | int(11)       | YES  |     | NULL    |                |
| codvend    | int(11)       | YES  |     | NULL    |                |
| presup     | int(11)       | YES  |     | NULL    |                |
| porcdto    | decimal(6,2)  | YES  |     | NULL    |                |
| moneda     | varchar(1)    | YES  |     | NULL    |                |
| cotiza     | decimal(12,5) | YES  |     | NULL    |                |
| bultos     | decimal(7,2)  | YES  |     | NULL    |                |
| pesoaprox  | decimal(8,2)  | YES  |     | NULL    |                |
| valoraprox | decimal(12,2) | YES  |     | NULL    |                |
| tte        | int(11)       | YES  |     | NULL    |                |
| impreso    | varchar(1)    | YES  |     | NULL    |                |
| estado     | varchar(1)    | YES  |     | NULL    |                |
| sucursal   | int(11)       | YES  | MUL | NULL    |                |
| observa    | varchar(30)   | YES  |     | NULL    |                |
| intfc      | int(11)       | YES  |     | NULL    |                |
| fe_arch    | date          | YES  |     | NULL    |                |
| nombre     | varchar(30)   | YES  |     | NULL    |                |
| domicilio  | varchar(20)   | YES  |     | NULL    |                |
| localidad  | varchar(20)   | YES  |     | NULL    |                |
| telefono   | varchar(30)   | YES  |     | NULL    |                |
| anulresp   | int(11)       | YES  |     | NULL    |                |
| anulfecha  | datetime      | YES  |     | NULL    |                |
+------------+---------------+------+-----+---------+----------------+

remito22
+-----------+---------------+------+-----+---------+----------------+
| Field     | Type          | Null | Key | Default | Extra          |
+-----------+---------------+------+-----+---------+----------------+
| id        | int(11)       | NO   | PRI | NULL    | auto_increment |
| nroint    | int(11)       | YES  | MUL | NULL    |                |
| item      | int(11)       | YES  |     | NULL    |                |
| idstk2    | int(11)       | YES  |     | NULL    |                |
| marca     | varchar(2)    | YES  | MUL | NULL    |                |
| codrep    | varchar(20)   | YES  |     | NULL    |                |
| desrep    | varchar(60)   | YES  |     | NULL    |                |
| tipoped   | varchar(1)    | YES  |     | NULL    |                |
| nrecep    | int(11)       | YES  |     | NULL    |                |
| cant      | decimal(7,2)  | YES  |     | NULL    |                |
| impunit   | decimal(12,2) | YES  |     | NULL    |                |
| dtounit   | decimal(6,2)  | YES  |     | NULL    |                |
| costounit | decimal(12,2) | YES  |     | NULL    |                |
| cantdev   | decimal(7,2)  | YES  |     | NULL    |                |
| nped      | int(11)       | YES  |     | NULL    |                |
| idclipe2  | int(11)       | YES  | MUL | NULL    |                |
| st        | varchar(1)    | YES  |     | NULL    |                |
| fe_arch   | date          | YES  |     | NULL    |                |
+-----------+---------------+------+-----+---------+----------------+


lispre
+-----------+---------------+------+-----+---------+-------+
| Field     | Type          | Null | Key | Default | Extra |
+-----------+---------------+------+-----+---------+-------+
| marca     | varchar(2)    | YES  | MUL | NULL    |       |
| codrep    | char(20)      | YES  |     | NULL    |       |
| vlpublico | decimal(12,2) | YES  |     | NULL    |       |
| coddescu  | varchar(4)    | YES  |     | NULL    |       |
| envase    | int(11)       | YES  |     | NULL    |       |
| desrep    | varchar(30)   | YES  |     | NULL    |       |
| fbaja     | date          | YES  |     | NULL    |       |
| codcambio | varchar(1)    | YES  |     | NULL    |       |
| reemplazo | char(20)      | YES  |     | NULL    |       |
| desreemp  | varchar(30)   | YES  |     | NULL    |       |
| codiva    | varchar(1)    | YES  |     | NULL    |       |
| codmargen | varchar(2)    | YES  |     | NULL    |       |
| margen    | decimal(6,2)  | YES  |     | NULL    |       |
| clasif    | varchar(3)    | YES  |     | NULL    |       |
| iva       | decimal(6,2)  | YES  |     | NULL    |       |
| vlconce   | decimal(12,2) | YES  |     | NULL    |       |
| grupo     | varchar(3)    | YES  |     | NULL    |       |
| basico    | varchar(8)    | YES  |     | NULL    |       |
| factor    | int(11)       | YES  |     | NULL    |       |
| moneda    | varchar(1)    | YES  |     | NULL    |       |
| fe_arch   | date          | YES  |     | NULL    |       |
+-----------+---------------+------+-----+---------+-------+



cliente0
+------------------------+--------------+------+-----+-------------------+-----------------------------+
| Field                  | Type         | Null | Key | Default           | Extra                       |
+------------------------+--------------+------+-----+-------------------+-----------------------------+
| cliente                | int(11)      | NO   | PRI | 0                 |                             |
| nombre                 | varchar(60)  | YES  |     | NULL              |                             |
| apellido               | varchar(30)  | YES  |     | NULL              |                             |
| nombres                | varchar(25)  | YES  |     | NULL              |                             |
| domcalle               | varchar(40)  | YES  |     | NULL              |                             |
| domnro                 | varchar(5)   | YES  |     | NULL              |                             |
| dompiso                | varchar(2)   | YES  |     | NULL              |                             |
| domdepto               | varchar(4)   | YES  |     | NULL              |                             |
| codpostal              | varchar(8)   | YES  |     | NULL              |                             |
| localidad              | varchar(25)  | YES  |     | NULL              |                             |
| provincia              | varchar(1)   | YES  |     | NULL              |                             |
| telefono               | varchar(20)  | YES  |     | NULL              |                             |
| telefono2              | varchar(20)  | YES  |     | NULL              |                             |
| fax                    | varchar(15)  | YES  |     | NULL              |                             |
| celucaract             | int(11)      | YES  |     | NULL              |                             |
| celunro                | bigint(20)   | YES  |     | NULL              |                             |
| tiene_email            | char(1)      | YES  |     | N                 |                             |
| email                  | varchar(100) | YES  | MUL | NULL              |                             |
| tipoiva                | varchar(3)   | YES  |     | NULL              |                             |
| cuit                   | bigint(20)   | YES  |     | NULL              |                             |
| exentoret              | varchar(1)   | YES  |     | NULL              |                             |
| zona                   | int(11)      | YES  | MUL | NULL              |                             |
| doctipo                | varchar(3)   | YES  |     | NULL              |                             |
| docnro                 | int(11)      | YES  |     | NULL              |                             |
| sexo                   | varchar(1)   | YES  |     | NULL              |                             |
| estcivil               | varchar(1)   | YES  |     | NULL              |                             |
| nacion                 | varchar(3)   | YES  |     | NULL              |                             |
| fenacim                | date         | YES  |     | NULL              |                             |
| tipo                   | varchar(1)   | YES  |     | NULL              |                             |
| sucursal               | int(11)      | YES  | MUL | NULL              |                             |
| estado                 | char(1)      | YES  | MUL | A                 |                             |
| share_with_dealer      | char(1)      | YES  |     | N                 |                             |
| share_with_corporation | char(1)      | YES  |     | N                 |                             |
| fe_arch                | date         | YES  |     | NULL              |                             |
| tiene_whatsapp         | char(1)      | YES  |     | NULL              |                             |
| idclienteclase         | int(11)      | YES  | MUL | 0                 |                             |
| app                    | tinyint(1)   | YES  |     | 0                 |                             |
| updated                | timestamp    | YES  |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| user                   | varchar(256) | YES  |     | NULL              |                             |
| password               | varchar(256) | YES  |     | NULL              |                             |
+------------------------+--------------+------+-----+-------------------+-----------------------------+


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
