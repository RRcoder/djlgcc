from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, FormView
from django.urls import reverse_lazy, reverse
from .models import ListaPrecios, Clientes, Procesos, Pedidos
from .forms import ListaPreciosForm, ClientesForm, CtaCteForm, CtaCteBlockForm, EntregaMercaderiaForm, EntregaMercaderiaDetForm
from .forms import GuardarPedidoForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, ExpressionWrapper, DecimalField, Func, Sum
from django.db.models.functions import Round
from django.views.decorators.http import require_POST

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


@require_POST
def guardar_pedido(request):
    form = GuardarPedidoForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/exito-extra/')






