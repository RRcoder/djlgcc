from django.urls import path
from django.views.generic import TemplateView
from .views import ListaPreciosCreateView, ListaPreciosListView, ListaPreciosUpdateView



urlpatterns = [
    path('cargar/', ListaPreciosCreateView.as_view(), name='crear_lista_precios'),
    path('ok/', TemplateView.as_view(template_name='ok.html'), name='lista_precios_ok'),
    path('listar/', ListaPreciosListView.as_view(), name='lista_precios_list'),
    path('editar/<int:pk>/', ListaPreciosUpdateView.as_view(), name='editar_lista_precios'),
    ]

