insert into cuentascorrientes_tiposcliente values (null, 'F', 'Persona Fisica');
insert into cuentascorrientes_tiposcliente values (null, 'J', 'Persona Juridica');

insert into cuentascorrientes_provincias values (null, 'B', 'Buenos Aires');


insert into cuentascorrientes_tiposdocumento values (null, 'DNI', 'Documento nacional de identidad');
insert into cuentascorrientes_tiposdocumento values (null, 'CUIT', 'Clave unica de identificacion tributaria');

al crear cliente check que tenga datos:
cuentascorrientes_tiposdocumento
cuentascorrientes_tiposcliente
cuentascorrientes_provincias


insert into empresa_datosusuarios values (null, 1, 2);
cuando crea pedido chequear q el usaurio tenga datos_usuarios cargados para q no se caiga

insert into cuentascorrientes_estadosped values (null, 'P', 'Pendiente');
insert into cuentascorrientes_estadosped values (null, 'E', 'Entregado');
cuando se guarda el ped pend chequear que este cargada la tabla estadosped


al pasar un ped pend a Entregado check que haya cargado
empresa_tiposcomprobante
empresa_comprobantes

insert into empresa_tiposcomprobante values (null, 'RM', 'Remito');
insert into empresa_comprobantes values (null, ' ', 10, 1,1,1);


ver de no dejar crear ni entregar pedidos si la cc esta bloqueada.




