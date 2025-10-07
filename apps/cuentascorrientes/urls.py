from django.urls import path
from django.views.generic import TemplateView
from .views import ListaPreciosCreateView, ListaPreciosListView, ListaPreciosUpdateView, AccionOk
from .views import ClientesCreateView, ClientesListView, ClientesUpdateView, AccionOk, CtaCteFormView
from .views import CtaCteBlockFormView, EntregaMercaderiaDetFormView, guardar_pedido, listado_pedidos, listado_pedidos_form
from .views import listado_pedidos_pendientes_form, listado_pedidos_pendientes

from .views import listado_pedidos_entregados, detalle_pedido

from .views import ingresar_pagos_form, entregar_pedido, rm_imprimir 

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
    path('entregamercaderia/<int:cliente_id>', EntregaMercaderiaDetFormView.as_view(), name='entrega_mercaderia'),
    path('entregamercaderia_form/<int:cliente_id>/<int:proceso_id>', EntregaMercaderiaDetFormView.as_view(), name='entrega_mercaderia_con_proceso_id'),

    path('guardar_pedido', guardar_pedido, name='guardar_pedido'),
    
    path('listado_pedidos_pendientes_form/', listado_pedidos_pendientes_form, name='listado_pedidos_pendientes_form'),
    path('listado_pedidos_pendientes_clie/', listado_pedidos_pendientes_form, name='listado_pedidos_pendientes_clie'),

    path('listado_pedidos_pendientes', listado_pedidos_pendientes, name='listado_pedidos_pendientes'),
    


    path('listado_pedidos_entregados', listado_pedidos_entregados, name='listado_pedidos_entregados'),
    path('listado_pedidos_form/', listado_pedidos_form, name='listado_pedidos_form'),

    path('ingresar_pagos_form/', ingresar_pagos_form, name='ingresar_pagos_form'),

    path('entregar_pedido/<int:pedido_id>', entregar_pedido, name='entregar_pedido'),

    path('detalle_pedido/<int:pk>', detalle_pedido, name='detalle_pedido'),





    # Listado de testeo
    path('listado_pedidos', listado_pedidos, name='listado_pedidos'),

    path("rm_imprimir/<int:remito_id>", rm_imprimir, name="rm_imprimir"),




    ]

