from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from .models import ListaPrecios, Clientes, Procesos, PedidosTmp, Remitos, RemitosDet, TiposDocumento, Estadosped, Pedidos, PedidosDet

from apps.empresa.models import DatosUsuarios, Comprobantes
from .forms import ListaPreciosForm, ClientesForm, CtaCteForm, CtaCteBlockForm, EntregaMercaderiaForm, EntregaMercaderiaDetForm, EntregaMercaderiaEditDetForm
from .forms import GuardarPedidoForm, ElegirClienteForm, IngresarComprobanteForm, InformePedidosForm, GuardarPedidoEditForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, DecimalField, Func, Sum, Max, Value, CharField, Count
from django.db.models.functions import Round, Coalesce, Concat, Cast
from django.views.decorators.http import require_POST

from django.db import transaction
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from datetime import date

#==================================================================================================
class ListaPreciosListView(LoginRequiredMixin, ListView):
    model = ListaPrecios
    template_name = 'lista_precios_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['codigo']  # Ordenar por código, podés cambiarlo

#==================================================================================================
class ListaPreciosCreateView(LoginRequiredMixin, CreateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/lista_precios_add.html'
    success_url = reverse_lazy('cuentascorrientes:accion_ok', kwargs={'titulo':"Alta Producto en Lista de precios OK"})

    def form_valid(self, form):
        # No guardamos todavía
        item = form.save(commit=False)

        item.codigo = item.codigo.upper()
        item.save()

        return super().form_valid(form)
#==================================================================================================
class ListaPreciosUpdateView(LoginRequiredMixin, UpdateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/lista_precios_edit.html'
    success_url = reverse_lazy('cuentascorrientes:lista_precios_list')  # Redirige al listado después de guardar

#==================================================================================================
@login_required
def AccionOk(request, titulo):
    return render(request, 'cuentascorrientes/accion_ok.html', context={'titulo':titulo})

#==================================================================================================
class ClientesListView(LoginRequiredMixin, ListView):
    model = Clientes
    template_name = 'clientes_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['nombre']

#==================================================================================================
class ClientesCreateView(LoginRequiredMixin, CreateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cuentascorrientes/clientes_add.html'
    success_url = reverse_lazy('cuentascorrientes:accion_ok', kwargs={'titulo':"Alta Cliente OK"})

    def form_valid(self, form):
        form.instance.activo = True  # valor por defecto oculto
        #print(form.cleaned_data)
        if form.cleaned_data.get('tipo').codigo =='F':
            td=TiposDocumento.objects.get(codigo='DNI')
            form.instance.tipo_documento=td
        else:
            td=TiposDocumento.objects.get(codigo='CUIT')
            form.instance.tipo_documento=td

        return super().form_valid(form)

#==================================================================================================
class ClientesUpdateView(LoginRequiredMixin, UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cuentascorrientes/clientes_edit.html'
    success_url = reverse_lazy('cuentascorrientes:clientes_list')

#==================================================================================================
@login_required
def inicio(request):
    context={}
    return render(request, 'inicio.html', context  )

#==================================================================================================
class CtaCteFormView(LoginRequiredMixin, UpdateView):
    model = Clientes
    template_name="cuentascorrientes/ctacte_form.html"
    form_class = CtaCteForm
    success_url = reverse_lazy('cuentascorrientes:clientes_list') 

    def form_valid(self, form):
        print(form)
        self.object=form.save(commit=False) # crea un objeto del modelo con los datos del form sin guardar para q luego podamos modificarlo y guarda lo que querramos.
        self.object.estadoctacte_id=1
        self.object.save()
        return super().form_valid(form)

#==================================================================================================
class CtaCteBlockFormView(LoginRequiredMixin, UpdateView):
    model = Clientes
    template_name="cuentascorrientes/ctacteblock_form.html"
    form_class = CtaCteBlockForm
    success_url = reverse_lazy('cuentascorrientes:clientes_list') 

    def form_valid(self, form):
        from datetime import date
        print(form)
        self.object=form.save(commit=False) # crea un objeto del modelo con los datos del form sin guardar para q luego podamos modificarlo y guarda lo que querramos.
        self.object.estadoctacte_id=2
        self.object.febaja=  date.today()
        self.object.save()
        return super().form_valid(form)

#==================================================================================================
class EntregaMercaderiaDetFormView(LoginRequiredMixin, FormView):
    template_name = 'cuentascorrientes/entrega_mercaderia_form.html'
    form_class = EntregaMercaderiaDetForm
    success_url = reverse_lazy('cuentascorrientes:entrega_mercaderia') # URL donde redirigir después de éxito

    def get_initial(self):
        initial = super().get_initial()
        # si en la url viene el parametro lo uso sino creo un ID de proceso nuevo en la DB
        proceso_id = self.kwargs.get('proceso_id')  # Si el parámetro viene por la URL
        cliente_id = self.kwargs.get('cliente_id')  # Si el parámetro viene por la URL
        print("------------")
        print("get initial")
        print(proceso_id)
        print(cliente_id)
        print("------------")
       
        initial['cliente_id']=cliente_id  #cargo el cliente_id del formulario con el valor de parametro en url

        if self.request.method == 'GET':
            if proceso_id:
                initial['proceso_id'] = proceso_id
            else:
                proc = Procesos(nombre="Pedido")
                proc.save()
                initial['proceso_id'] = proc.id

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print("==== context")
        proceso_id = self.kwargs.get('proceso_id')  # Si el parámetro viene por la URL
        print(proceso_id)
        cliente_id = self.kwargs.get('cliente_id')  # Si el parámetro viene por la URL
            
        p = PedidosTmp.objects.filter(proceso_id=proceso_id).annotate(
        total=ExpressionWrapper(Func(F('precio') * F('cantidad'), 2, function='round'),
        output_field=DecimalField(max_digits=12, decimal_places=2))
        )

        totales = PedidosTmp.objects.filter(proceso_id=proceso_id).aggregate(total=Sum(
        ExpressionWrapper(Func(F('precio') * F('cantidad'), 2, function='round'), output_field=DecimalField())
        ))
        #print(totales.query)

        cliente = Clientes.objects.get(id=cliente_id)

        print(p.query)
        context['cliente']= cliente
        context['datos_adic']= p
        context['totales']= totales
        context['form_extra']= GuardarPedidoForm(initial={'proceso_id':proceso_id, 'cliente_id':cliente_id})

        print(p)
        print("====")

        return context

    def form_valid(self, form):
        # Lógica para procesar el formulario y guardar los datos
        p = form.cleaned_data['producto']
        cantidad = form.cleaned_data['cantidad']

        ped = PedidosTmp(proceso_id=form.cleaned_data['proceso_id'])

        #print(form.cleaned_data)
        user=self.request.user
        datos_usuario = user.datos_usuario.get()

        print( user)
        ped.fecha         = date.today()
        ped.cliente_id    = form.cleaned_data['cliente_id']
        ped.sucursal      = datos_usuario.sucursal
        ped.codigo        = p.codigo
        ped.descripcion   = p.descripcion
        ped.precio        = p.precio
        ped.costo         = p.costo
        ped.cantidad      = form.cleaned_data['cantidad']
        #ped.alicuota_iva  = form.cleaned_data['']
        ped.rm_realizado = 0
        ped.save()

        print("------------")
        print("VALID")
        print(form.cleaned_data)
        print("------------")
        #En el propio objeto Formview podria guardar todo el form o solo el dato del proceso_id, guardo el dato para poder usarlo en el 
        # get_success_url
        self.proceso_id=form.cleaned_data['proceso_id']
        self.cliente_id=form.cleaned_data['cliente_id']

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        print("==============")
        print("SUCESS")
        print(self.proceso_id)
        print("==============")
        return reverse_lazy('cuentascorrientes:entrega_mercaderia_con_proceso_id', kwargs={'proceso_id': self.proceso_id, 'cliente_id': self.cliente_id})

#==================================================================================================
@login_required
@require_POST
def guardar_pedido(request):
    user = request.user

    form = GuardarPedidoForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data['proceso_id'])
        print(form.cleaned_data['cliente_id'])

        # Creo un Pedido y un Detalle. Esto me va dar un numero de pedido que va estar en estado PENDIENTE
        # Luego cuando creo el RM para a ENTREGADO

        pedidos = PedidosTmp.objects.filter(proceso_id = form.cleaned_data['proceso_id'])
        
        estado_pedido= Estadosped.objects.get(codigo='P')

        p = Pedidos.objects.create(
            fecha = date.today(),
            cliente_id = pedidos[0].cliente_id,
            sucursal_id = pedidos[0].sucursal_id,
            rm_realizado = 0,
            estado = estado_pedido ,
            usuario = user
        )

        print('====---')
        print(p.id)

        detalle_pedido = [
            PedidosDet(
                pedido_id       = p.id,
                codigo          = pedido.codigo,
                descripcion     = pedido.descripcion,
                importe_unitario= pedido.precio,
                costo           = pedido.costo,
                cantidad        = pedido.cantidad,
            )
            for pedido in pedidos
        ]
        PedidosDet.objects.bulk_create(detalle_pedido)

        return redirect('cuentascorrientes:accion_ok', titulo='Pedido Registrado satisfactoriamente')
    else:
        print("fuuuck")
        print(form.errors)

#==================================================================================================
@login_required
def listado_pedidos_form(request):
    if request.method == 'POST':
        form = ElegirClienteForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['cliente']
            cliente_id=c.id
            cliente = get_object_or_404(Clientes, pk=cliente_id)

            #movimientos = RemitosDet.objects.filter(remito__cliente_id=3).values('remito_id').annotate(imptotal = Sum('importe_unitario')).order_by('remito__fecha')
            movimientos = Remitos.objects.filter(cliente_id=cliente_id).annotate(
                total=Sum(
                    ExpressionWrapper(
                        F('remitosdet__importe_unitario')  * F('remitosdet__cantidad'),
                        output_field=DecimalField(max_digits=14, decimal_places=2)
                    )
                ),
                comprobante=Concat(
                Value('RM '),
                Cast('punto_de_venta', CharField()),
                Value('-'),
                Cast('numero', CharField())
            )
            ).order_by('fecha','punto_de_venta', 'numero')
            print(movimientos.query)
            #saldo = movimientos.aggregate(suma=Sum('monto'))['suma'] or 0

            suma_total = Remitos.objects.filter(cliente_id=cliente_id).aggregate(
                total_general=Sum(
                    ExpressionWrapper(
                        F('remitosdet__importe_unitario') * F('remitosdet__cantidad'),
                        output_field=DecimalField(max_digits=14, decimal_places=2)
                    )
                )
            )['total_general']

            contexto = {
                'cliente': cliente,
                'objects': movimientos,
                'suma_total': suma_total
            }

            return render(request, 'cuentascorrientes/listado_pedidos.html', contexto)

            #return render(request, 'formulario_exito.html', {'nombre': nombre})
    else:
        form = ElegirClienteForm()
    
    return render(request, 'cuentascorrientes/elegir_cliente_form.html', {'form': form})
#==================================================================================================
@login_required
def listado_pedidos(request):
    cliente_id=3
    cliente = get_object_or_404(Clientes, pk=cliente_id)

    #movimientos = RemitosDet.objects.filter(remito__cliente_id=3).values('remito_id').annotate(imptotal = Sum('importe_unitario')).order_by('remito__fecha')
    movimientos = Remitos.objects.filter(cliente_id=3).annotate(
        total=Sum(
            ExpressionWrapper(
                F('remitosdet__importe_unitario')  * F('remitosdet__cantidad'),
                output_field=DecimalField(max_digits=14, decimal_places=2)
            )
        ),
        comprobante=Concat(
        Value('RM '),
        Cast('punto_de_venta', CharField()),
        Value('-'),
        Cast('numero', CharField())
    )
    ).order_by('fecha','punto_de_venta', 'numero')
    print(movimientos.query)
    #saldo = movimientos.aggregate(suma=Sum('monto'))['suma'] or 0

    suma_total = Remitos.objects.filter(cliente_id=3).aggregate(
        total_general=Sum(
            ExpressionWrapper(
                F('remitosdet__importe_unitario') * F('remitosdet__cantidad'),
                output_field=DecimalField(max_digits=14, decimal_places=2)
            )
        )
    )['total_general']

    contexto = {
        'cliente': cliente,
        'objects': movimientos,
        'suma_total': suma_total
    }

    return render(request, 'cuentascorrientes/listado_pedidos.html', contexto)

#==================================================================================================
@login_required
def ingresar_pagos_form(request):
    if request.method == 'POST':
        print('')
        form = IngresarComprobanteForm(request.POST)
        if not form.is_valid():
            print('eerror en el form')
            print(form.errors)
        else:
            #c = form.cleaned_data['cliente']
            print(form.cleaned_data)

            #contexto = {
                #'cliente': cliente,
                #'objects': movimientos,
                #'suma_total': suma_total
            #}

            #return render(request, 'cuentascorrientes/listado_pedidos.html', contexto)




            ##return render(request, 'formulario_exito.html', {'nombre': nombre})
    else:
        form = IngresarComprobanteForm(initial={'id_pedido':13})
        return render(request, 'cuentascorrientes/ingresar_comprobante_form.html', {'form': form})

#==================================================================================================
@login_required
def listado_pedidos_pendientes_form(request):

    cliente_id=None
    
    if request.method == 'POST':
        form = ElegirClienteForm(request.POST)
        if form.is_valid():
            c = form.cleaned_data['cliente']
            cliente_id=c.id
            cliente = get_object_or_404(Clientes, pk=cliente_id)
        else:
            return render(request, 'cuentascorrientes/listado_pedidos_pendientes_clie.html', contexto)
    else:
        cliente_id = request.GET.get('cliente_id')

    # Si tenemos un cliente válido (por GET o POST), mostramos sus pedidos
    if cliente_id:

        try:
            cliente = Clientes.objects.get(id=cliente_id)
        except Clientes.DoesNotExist:
            return redirect('cuentascorrientes:accion_ok', titulo='Cliente no encontrado!')

        movimientos = Pedidos.objects.filter(cliente_id=cliente_id, estado_id=1).annotate(
            total_items=Count('detalles'),
            total_kg=Sum('detalles__cantidad'),
            total_importe=Sum(
                F('detalles__cantidad') * F('detalles__importe_unitario'),
                output_field=DecimalField()
                )
        )

        contexto = {
            'cliente': cliente,
            'objects': movimientos,
            'suma_total': 0
        }

        return render(request, 'cuentascorrientes/listado_pedidos_pendientes_clie.html', contexto)
    else:
        form = ElegirClienteForm()
        return render(request, 'cuentascorrientes/elegir_cliente_form.html', {'form': form, 'titulo': "Listado de pedidos pendientes"})

#==============================================================================
@login_required
def listado_pedidos_pendientes(request):
    
    movimientos = Pedidos.objects.filter(estado_id=1).annotate(
        total_items=Count('detalles'),
        total_kg=Sum('detalles__cantidad'),
        total_importe=Sum(
            F('detalles__cantidad') * F('detalles__importe_unitario'),
            output_field=DecimalField()
            )
    )

    #contexto = {
        #'objects': movimientos,
        #'suma_total': 0
    #}
    #movimientos = Remitos.objects.filter(cliente_id=cliente_id).annotate(
        #total=Sum(
            #ExpressionWrapper(
                #F('remitosdet__importe_unitario')  * F('remitosdet__cantidad'),
                #output_field=DecimalField(max_digits=14, decimal_places=2)
            #)
        #),
        #comprobante=Concat(
        #Value('RM '),
        #Cast('punto_de_venta', CharField()),
        #Value('-'),
        #Cast('numero', CharField())
    #)
    #).order_by('fecha','punto_de_venta', 'numero')
    #print(movimientos.query)
    ##saldo = movimientos.aggregate(suma=Sum('monto'))['suma'] or 0

    #suma_total = Remitos.objects.filter(cliente_id=cliente_id).aggregate(
        #total_general=Sum(
            #ExpressionWrapper(
                #F('remitosdet__importe_unitario') * F('remitosdet__cantidad'),
                #output_field=DecimalField(max_digits=14, decimal_places=2)
            #)
        #)
    #)['total_general']

    contexto = {
        'objects': movimientos,
    }

    return render(request, 'cuentascorrientes/listado_pedidos_pendientes.html', contexto)

#==============================================================================
@login_required
def listado_pedidos_entregados(request):
    
    movimientos = Pedidos.objects.filter(estado_id=2).annotate(
        total_items=Count('detalles'),
        total_kg=Sum('detalles__cantidad'),
        total_importe=Sum(
            F('detalles__cantidad') * F('detalles__importe_unitario'),
            output_field=DecimalField()
            )
    )

    contexto = {
        'objects': movimientos,
    }

    return render(request, 'cuentascorrientes/listado_pedidos_entregados.html', contexto)
#==============================================================================
@login_required
def entregar_pedido(request, pedido_id):
    #entregar un pedido genera el RM y cambia de estado el pedido a Entregado

    user=request.user


    try:
        pedido = Pedidos.objects.get(id=pedido_id)
    except Pedidos.DoesNotExist:
        return redirect('cuentascorrientes:accion_ok', titulo='Pedido no encontrado!')

    print("---------***--------")
    print(pedido)
    
    #con los datos del usuario determino en que sucursal trabaja. un usuario no puede estar en dos sucursales.
    # si se necesita que este en dos sucursales se crea otro usuario con acceso a esa otra sucursal y listo.
    du = DatosUsuarios.objects.filter(usuario_id=user).first()
    #print(du.sucursal.id)
    datos_comprobante = Comprobantes.objects.filter(comprobante__nombre='RM').first()

    print(datos_comprobante)
    print('?'*30)
    
    if pedido.rm_realizado==1:
        #redirecciono, ya esta hecho el RM en este pedido
        return redirect('cuentascorrientes:accion_ok', titulo='El pedido ya tiene RM registrado!!')


    ultimo = Remitos.objects.aggregate(Max('numero'))['numero__max']

    try:
        with transaction.atomic():
            rm=Remitos()
            rm.fecha=date.today()
            rm.punto_de_venta=datos_comprobante.punto_de_venta
            rm.numero= (ultimo or 0) + 1
            rm.cliente_id= pedido.cliente_id
            rm.sucursal_id= du.sucursal.id
            rm.usuario = user 
            rm.save()

            detalle = PedidosDet.objects.filter(pedido_id = pedido_id)

            detalles = [
                RemitosDet(
                    remito          = rm,
                    codigo          = linea.codigo,
                    descripcion     = linea.descripcion,
                    importe_unitario= linea.importe_unitario,
                    costo           = linea.costo,
                    cantidad        = linea.cantidad,
                    alicuota_iva    = None,
                    dtounit         = 0,
                    importe_iva     = 0
                )
                for linea in detalle
            ]
                
            RemitosDet.objects.bulk_create(detalles)

            pedido.rm_realizado=1
            pedido.estado_id=2
            pedido.rm_asociado= rm
            pedido.save()
    except Exception as e:
        return redirect('cuentascorrientes:accion_ok', titulo=f"Error al generar el RM. Codigo de error {str(e)}")

    return redirect('cuentascorrientes:accion_ok', titulo="El egreso fue registrado correctamente.")

#==================================================================================================
@login_required
def detalle_pedido(request, pk):
    pedido = get_object_or_404(Pedidos.objects.select_related('cliente', 'sucursal', 'estado', 'rm_asociado', 'usuario'), pk=pk)
    detalles = pedido.detalles.all()  # gracias a `related_name='detalles'`

    #form = AgregarMercaderiaForm()
    form = None

    return render(request, 'cuentascorrientes/pedido_detalle.html', {
        'pedido': pedido,
        'detalles': detalles,
        'form': form
    })
#==================================================================================================
@login_required
def rm_imprimir(request, remito_id):
    comprobante = Remitos.objects.annotate(
        total_general=Sum(
            ExpressionWrapper(F('detalles__importe_unitario') * F('detalles__cantidad'),
            output_field=DecimalField()
            )
        )
    ).get(id=remito_id)
    #.annotate(
        #total=Sum(
            #ExpressionWrapper(
                #F('remitosdet__importe_unitario')  * F('remitosdet__cantidad'),
                #output_field=DecimalField(max_digits=14, decimal_places=2)
            #)
        #),
        #comprobante=Concat(
        #Value('RM '),
        #Cast('punto_de_venta', CharField()),
        #Value('-'),
        #Cast('numero', CharField())
    #)
    #).order_by('fecha','punto_de_venta', 'numero')

    print("))))))))))))))))))))))")
    print(comprobante)

    print(    comprobante.detalles.all())


    #remito = get_object_or_404(Remitos, pk=remito_id)
    return render(request, "cuentascorrientes/rm_imprimir.html", {"remito": comprobante, 'objects_det': comprobante.detalles.all()})

#==================================================================================================
@login_required
def pedido_eliminar(request, pedido_id):
    pedido = get_object_or_404(Pedidos.objects.select_related('cliente', 'sucursal', 'estado', 'rm_asociado', 'usuario'), id=pedido_id)
    detalles = pedido.detalles.all()  # gracias a `related_name='detalles'`

    if request.method == 'POST':
        pedido.delete()
        messages.success(request, "El pedido fue eliminado exitosamente.")
        return redirect('cuentascorrientes:listado_pedidos_pendientes')

    return render(request, 'cuentascorrientes/pedido_eliminar.html', {'pedido': pedido, 'detalles': detalles})


#==================================================================================================
def informe_pedidos(request):
    # Si el formulario es enviado
    if request.method == 'GET':
        form = InformePedidosForm()
        return render(request, 'cuentascorrientes/informe_pedidos_form.html', {'form': form})
    else:
        form = InformePedidosForm(request.POST)
        
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']

            # Filtramos los pedidos con los parámetros
            pedidos = Pedidos.objects.filter(
                cliente=cliente,
                estado__codigo='E',  # Asumiendo que "codigo" es el campo que contiene el estado 'E'
                fecha__range=[fecha_desde, fecha_hasta]
            ).select_related('cliente', 'estado', 'sucursal').order_by('fecha').annotate(
                total_remitos=Sum(
                ExpressionWrapper(
                    F('rm_asociado__detalles__importe_unitario') * F('rm_asociado__detalles__cantidad'),
                    output_field=DecimalField()
                )
                )
            )

            return render(request, 'cuentascorrientes/informe_pedidos.html', {
                'form': form,
                'pedidos': pedidos
            })
#==================================================================================================
@login_required
def pedido_editar(request, pedido_id):
    """
        Voy a crear un id de proceso nuevo y cargar todo el pedido a la tabla pedidos tmp y que modifique 
        todo lo que quiera. Con el boton Guardar Cambios meto todo en el pedido original.

    """
    #busco el pedido y el detalle
    pedido= Pedidos.objects.get(id=pedido_id)
    pedido_detalle= pedido.detalles.all()

    with transaction.atomic():
        #creo un proceso
        proc = Procesos(nombre="Pedido")
        proc.save()

        #Creo el pedidotmp
        ped = PedidosTmp(proceso_id=proc.id, fecha=pedido.fecha, cliente=pedido.cliente, sucursal=pedido.sucursal, rm_realizado=pedido.rm_realizado)

        regs_pedidotmp = [
            PedidosTmp(
                fecha       = pedido.fecha, 
                proceso_id  = proc.id, 
                cliente     = pedido.cliente, 
                sucursal    = pedido.sucursal, 
                codigo      = linea.codigo,
            descripcion = linea.descripcion,
            precio      = linea.importe_unitario,
                costo       = linea.costo,
                cantidad    = linea.cantidad,
                alicuota_iva=0,
                rm_realizado=pedido.rm_realizado,
                edit_id     = pedido.id                #guardo el id para saber sobre que pedido lo tengo que guardar cuando salve los cambios.
            )
            for linea in pedido_detalle
        ]
        
        PedidosTmp.objects.bulk_create(regs_pedidotmp)

    #aca ya tengo todo en TMP le dejo editar

    #user=request.user
    #datos_usuario = user.datos_usuario.get()

    ##if request.method == 'POST':
        ##pedido.delete()
        ##messages.success(request, "El pedido fue eliminado exitosamente.")
        ##return redirect('lista_pedidos')  # Cambia esto a la vista/listado que tengas
        

    return redirect('cuentascorrientes:entrega_mercaderia_edit_con_proceso_id', cliente_id=pedido.cliente_id , proceso_id=proc.id)


@transaction.atomic
def tmp_editar(request):
    if request.method == 'POST':
        tmp = get_object_or_404(PedidosTmp, id=request.POST['tmp_id'])
        tmp.cantidad = request.POST['cantidad']
        tmp.save()

    return redirect(request.META.get('HTTP_REFERER', '/'))

@transaction.atomic
def tmp_eliminar(request, id):
    tmp = get_object_or_404(PedidosTmp, id=id)
    tmp.delete()

    return redirect(request.META.get('HTTP_REFERER', '/'))


class EntregaMercaderiaEditDetFormView(LoginRequiredMixin, FormView):
    template_name = 'cuentascorrientes/entrega_mercaderia_edit_form.html'
    form_class = EntregaMercaderiaEditDetForm
    success_url = reverse_lazy('cuentascorrientes:entrega_mercaderia_edit_con_proceso_id') # URL donde redirigir después de éxito

    def get_initial(self):
        initial = super().get_initial()
        # si en la url viene el parametro lo uso sino creo un ID de proceso nuevo en la DB
        proceso_id = self.kwargs.get('proceso_id')  # Si el parámetro viene por la URL
        cliente_id = self.kwargs.get('cliente_id')  # Si el parámetro viene por la URL
        print("------------")
        print("get initial")
        print(proceso_id)
        print(cliente_id)
        print("------------")
       
        initial['cliente_id']=cliente_id  #cargo el cliente_id del formulario con el valor de parametro en url

        if self.request.method == 'GET':
            if proceso_id:
                initial['proceso_id'] = proceso_id
            else:
                proc = Procesos(nombre="Pedido")
                proc.save()
                initial['proceso_id'] = proc.id

        return initial

    def get_context_data(self, **kwargs):   #arma el array para pasarle de contexto al template
        context = super().get_context_data(**kwargs)
        print("==== context")
        proceso_id = self.kwargs.get('proceso_id')  # Si el parámetro viene por la URL
        print(proceso_id)
        cliente_id = self.kwargs.get('cliente_id')  # Si el parámetro viene por la URL
            
        p = PedidosTmp.objects.filter(proceso_id=proceso_id).annotate(
        total=ExpressionWrapper(Func(F('precio') * F('cantidad'), 2, function='round'),
        output_field=DecimalField(max_digits=12, decimal_places=2))
        )

        totales = PedidosTmp.objects.filter(proceso_id=proceso_id).aggregate(total=Sum(
        ExpressionWrapper(Func(F('precio') * F('cantidad'), 2, function='round'), output_field=DecimalField())
        ))
        #print(totales.query)
        #puedo tomar el id del pedido original q estoy editando de cualquier registro, todos lo tienen.
        pedido_orig_id=p[0].edit_id


        cliente = Clientes.objects.get(id=cliente_id)

        print(p.query)
        context['cliente']= cliente
        context['datos_adic']= p
        context['totales']= totales
        context['form_extra']= GuardarPedidoEditForm(initial={'proceso_id':proceso_id, 'cliente_id':cliente_id})
        context['pedido_orig_id']= pedido_orig_id

        print(p)
        print("====")

        return context

    def form_valid(self, form):
        # Lógica para procesar el formulario y guardar los datos
        p = form.cleaned_data['producto']
        cantidad = form.cleaned_data['cantidad']

        ped = PedidosTmp(proceso_id=form.cleaned_data['proceso_id'])

        #print(form.cleaned_data)
        user=self.request.user
        datos_usuario = user.datos_usuario.get()

        print( user)
        ped.fecha         = date.today()
        ped.cliente_id    = form.cleaned_data['cliente_id']
        ped.sucursal      = datos_usuario.sucursal
        ped.codigo        = p.codigo
        ped.descripcion   = p.descripcion
        ped.precio        = p.precio
        ped.costo         = p.costo
        ped.cantidad      = form.cleaned_data['cantidad']
        #ped.alicuota_iva  = form.cleaned_data['']
        ped.rm_realizado  = 0
        ped.edit_id       = form.cleaned_data['pedido_orig_id']
        ped.save()

        print("------------")
        print("VALID")
        print(form.cleaned_data)
        print("------------")
        #En el propio objeto Formview podria guardar todo el form o solo el dato del proceso_id, guardo el dato para poder usarlo en el 
        # get_success_url porque necesito esos dos datos para armar el url
        self.proceso_id=form.cleaned_data['proceso_id']
        self.cliente_id=form.cleaned_data['cliente_id']

        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        print("==============")
        print("SUCESS")
        print(self.proceso_id)
        print("==============")
        return reverse_lazy('cuentascorrientes:entrega_mercaderia_edit_con_proceso_id', kwargs={'proceso_id': self.proceso_id, 'cliente_id': self.cliente_id})

#==================================================================================================
@login_required
@require_POST
def guardar_pedido_edit(request):
    #este guardar es distinto al del crear un pedido porque es edicion, el pedido esta creado lo que se hace ahora 
    # es borrar el detalle y poner todo lo que hay en pedidostmp
    user = request.user

    form = GuardarPedidoEditForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data['proceso_id'])
        print(form.cleaned_data['cliente_id'])

        pedidostmp = PedidosTmp.objects.filter(proceso_id = form.cleaned_data['proceso_id'])
        pedido_id=pedidostmp[0].edit_id

        with transaction.atomic():
            #borro todo el detalle y luego inserto lo q hay en pedidostmp
            pedidos = PedidosDet.objects.filter(pedido_id = pedido_id)
            pedidos.delete()


            detalle_pedido = [
                PedidosDet(
                    pedido_id       = pedido_id,
                    codigo          = pedido.codigo,
                    descripcion     = pedido.descripcion,
                    importe_unitario= pedido.precio,
                    costo           = pedido.costo,
                    cantidad        = pedido.cantidad,
                )
                for pedido in pedidostmp
            ]
            
            PedidosDet.objects.bulk_create(detalle_pedido)
        return redirect('cuentascorrientes:accion_ok', titulo='Pedido Modificado satisfactoriamente')
    else:
        print("fuuuck")
        print(form.errors)






