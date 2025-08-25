from django.urls import path
from django.views.generic import TemplateView
from .views import ListaPreciosCreateView, ListaPreciosListView, ListaPreciosUpdateView, AccionOk
from .views import ClientesCreateView, ClientesListView, ClientesUpdateView, AccionOk, CtaCteFormView
from .views import CtaCteBlockFormView

app_name="cuentascorrientes"

urlpatterns = [
    path('lista_precios_list', ListaPreciosListView.as_view(), name='lista_precios_list'),
    path('lista_precios_edit/<int:pk>/', ListaPreciosUpdateView.as_view(), name='lista_precios_edit'),
    path('cargar/', ListaPreciosCreateView.as_view(), name='lista_precios_add'),
    path('ok/', TemplateView.as_view(template_name='ok.html'), name='lista_precios_ok'),
    path('accion_ok/<str:titulo>', AccionOk, name='accion_ok'),

    path('clientes_list', ClientesListView.as_view(), name='clientes_list'),
    path('clientes_add/', ClientesCreateView.as_view(), name='clientes_add'),
    path('clientes_edit/<int:pk>/', ClientesUpdateView.as_view(), name='clientes_edit'),
    path('cuentascorrientes/<int:pk>/', CtaCteFormView.as_view(), name='ctacte'),
    path('cuentascorrientes_block/<int:pk>/', CtaCteBlockFormView.as_view(), name='ctacte_bloquear'),


    ]

