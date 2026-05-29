from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('productos/', views.producto_lista, name='producto_lista'),
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('proveedores/', views.proveedor_lista, name='proveedor_lista'),
]
