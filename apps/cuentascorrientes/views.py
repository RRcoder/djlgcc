from django.shortcuts import render

from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from .models import ListaPrecios
from .forms import ListaPreciosForm


class ListaPreciosListView(ListView):
    model = ListaPrecios
    template_name = 'lista_precios_list.html'  # Ruta al template
    context_object_name = 'items'  # Nombre del objeto en el template
    ordering = ['codigo']  # Ordenar por código, podés cambiarlo


class ListaPreciosCreateView(CreateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/crear_lista_precios.html'
    success_url = reverse_lazy('cuentascorrientes/lista_precios_ok')  # Asegurate de tener esta URL definida


class ListaPreciosUpdateView(UpdateView):
    model = ListaPrecios
    form_class = ListaPreciosForm
    template_name = 'cuentascorrientes/editar_lista_precios.html'
    success_url = reverse_lazy('lista_precios_list')  # Redirige al listado después de guardar

