from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .models import ListaPrecios, Clientes
from .forms import ListaPreciosForm, ClientesForm


class ListaPreciosListView(ListView):
    model = ListaPrecios
    template_name = 'lista_precios_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['codigo']  # Ordenar por código, podés cambiarlo


class ListaPreciosCreateView(CreateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/crear_lista_precios.html'
    success_url = reverse_lazy('cuentascorrientes:accion_ok', kwargs={'titulo':"Alta Producto en Lista de precios OK"})


class ListaPreciosUpdateView(UpdateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/editar_lista_precios.html'
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


class ClientesUpdateView(UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'cuentascorrientes/clientes_edit.html'
    success_url = reverse_lazy('cuentascorrientes:clientes_list')

