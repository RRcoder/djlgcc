from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from .models import ListaPrecios, Clientes, Procesos, Pedidos, Remitos, RemitosDet

from apps.empresa.models import DatosUsuarios, Comprobantes
from .forms import ListaPreciosForm, ClientesForm, CtaCteForm, CtaCteBlockForm, EntregaMercaderiaForm, EntregaMercaderiaDetForm
from .forms import GuardarPedidoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, DecimalField, Func, Sum, Max
from django.db.models.functions import Round
from django.views.decorators.http import require_POST

from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required

from datetime import date

class ListaPreciosListView(LoginRequiredMixin, ListView):
    model = ListaPrecios
    template_name = 'lista_precios_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['codigo']  # Ordenar por código, podés cambiarlo


class ListaPreciosCreateView(CreateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/lista_precios_add.html'
    success_url = reverse_lazy('cuentascorrientes:accion_ok', kwargs={'titulo':"Alta Producto en Lista de precios OK"})


class ListaPreciosUpdateView(UpdateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/lista_precios_edit.html'
    success_url = reverse_lazy('cuentascorrientes:lista_precios_list')  # Redirige al listado después de guardar

def AccionOk(request, titulo):
    return render(request, 'cuentascorrientes/accion_ok.html', context={'titulo':titulo})

class ClientesListView(ListView):
    model = Clientes
    template_name = 'clientes_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['id']  # Ordenar por código, podés cambiarlo 

class ClientesCreateView(CreateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cuentascorrientes/clientes_add.html'
    success_url = reverse_lazy('cuentascorrientes:accion_ok', kwargs={'titulo':"Alta Cliente OK"})

    def form_valid(self, form):
        form.instance.activo = True  # valor por defecto oculto
        return super().form_valid(form)

class ClientesUpdateView(UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cuentascorrientes/clientes_edit.html'
    success_url = reverse_lazy('cuentascorrientes:clientes_list')


def inicio(request):

    context={}
    return render(request, 'inicio.html', context  )

class CtaCteFormView(UpdateView):
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

class CtaCteBlockFormView(UpdateView):
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


class EntregaMercaderiaDetFormView(FormView):
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
            
        p = Pedidos.objects.filter(proceso_id=proceso_id).annotate(
        total=ExpressionWrapper(Func(F('precio') * F('cantidad'), 2, function='round'),
        output_field=DecimalField(max_digits=12, decimal_places=2))
        )

        totales = Pedidos.objects.filter(proceso_id=proceso_id).aggregate(total=Sum(
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

        ped = Pedidos(proceso_id=form.cleaned_data['proceso_id'])

        #ped.fecha         = form.cleaned_data['']
        #ped.cliente       = form.cleaned_data['']
        #ped.sucursal      = form.cleaned_data['']
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


@login_required
@require_POST
def guardar_pedido(request):
    user = request.user

    form = GuardarPedidoForm(request.POST)
    if form.is_valid():
        print(form.cleaned_data['proceso_id'])
        print(form.cleaned_data['cliente_id'])

        #con los datos del usuario determino en que sucursal trabaja. un usuario no puede estar en dos sucursales.
        # si se necesita que este en dos sucursales se crea otro usuario con acceso a esa otra sucursal y listo.
        du = DatosUsuarios.objects.filter(usuario_id=user).first()
        #print(du.sucursal.id)
        datos_comprobante = Comprobantes.objects.filter(comprobante__nombre='RM').first()

        print(datos_comprobante)
        print('?'*30)

        ultimo = Remitos.objects.aggregate(Max('numero'))['numero__max']
        rm=Remitos()
        rm.fecha=date.today()
        rm.punto_de_venta=datos_comprobante.punto_de_venta
        rm.numero= (ultimo or 0) + 1
        rm.cliente_id=form.cleaned_data['cliente_id']
        rm.sucursal_id= du.sucursal.id
        rm.save()

        pedidos = Pedidos.objects.filter(proceso_id = form.cleaned_data['proceso_id'])

        detalles = [
            RemitosDet(
                remito          = rm,
                codigo          = pedido.codigo,
                descripcion     = pedido.descripcion,
                importe_unitario= pedido.precio,
                costo           = pedido.costo,
                cantidad        = pedido.cantidad,
                alicuota_iva    = pedido.alicuota_iva,
                dtounit         = 0,
                importe_iva     = 0
            )
            for pedido in pedidos
        ]
        
        RemitosDet.objects.bulk_create(detalles)

        pedidos.update(rm_realizado=1)


        print("OKKKK")

    else:
        print("fuuuck")
        print(form.errors)





def resumen_de_cuenta(request):
    cliente_id=3
    cliente = get_object_or_404(Clientes, pk=cliente_id)

    movimientos = RemitosDet.objects.filter(remito__cliente_id=3).values('remito_id').annotate(imptotal = Sum('importe_unitario')).order_by('remito__fecha')

    print(movimientos.query)
    #saldo = movimientos.aggregate(suma=Sum('monto'))['suma'] or 0

    contexto = {
        'cliente': cliente,
        'objects': movimientos,
        #'saldo': saldo
    }

    return render(request, 'cuentascorrientes/resumen_de_cuenta.html', contexto)

