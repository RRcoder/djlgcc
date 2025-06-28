from django.db import models


class TiposCliente(models.Model):
    codigo                 = models.CharField(max_length=1)
    descripcion            = models.CharField(max_length=50)

class Provincias(models.Model):
    codigo        = models.CharField(max_length=1)
    nombre        = models.CharField(max_length=100)



class Clientes(models.Model):
    nombre                 = models.CharField(max_length=200)
    domicilio_calle        = models.CharField(max_length=200)
    domicilio_numero       = models.CharField(max_length=10)
    domicilio_piso         = models.CharField(max_length=10)
    domicilio_departamento = models.CharField(max_length=10) 
    codigo_postal          = models.CharField(max_length=10) 
    localidad              = models.CharField(max_length=200)
    provincia              = models.ForeignKey('Provincias', on_delete=models.PROTECT, blank=True, null=True) 
    telefono_fijo          = models.CharField(max_length=50)
    telefono_celular       = models.CharField(max_length=10)
    email                  = models.EmailField(blank=True, null=True) 
    cuit                   = models.BigIntegerField() 
    tipo                   = models.ForeignKey('TiposCliente', on_delete=models.PROTECT, blank=True, null=True) 
    sucursal               = models.ForeignKey('empresa.Sucursales', on_delete=models.PROTECT, blank=True, null=True)
    activo                 = models.BooleanField() 
    updated                = models.DateTimeField(auto_now=True)
    created                = models.DateTimeField(auto_now_add=True)




















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


"""
