from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    # Categorías
    path('categorias/', views.categoria_lista, name='categoria_lista'),
    path('categorias/nueva/', views.categoria_crear, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_editar, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_eliminar, name='categoria_eliminar'),

    # Productos
    path('productos/', views.producto_lista, name='producto_lista'),
    path('productos/buscar/', views.producto_buscar, name='producto_buscar'),
    path('productos/importar/', views.producto_importar_csv, name='producto_importar_csv'),
    path('productos/nuevo/', views.producto_crear, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),

    # Proveedores
    path('proveedores/', views.proveedor_lista, name='proveedor_lista'),
    path('proveedores/nuevo/', views.proveedor_crear, name='proveedor_crear'),
    path('proveedores/<int:pk>/editar/', views.proveedor_editar, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_eliminar, name='proveedor_eliminar'),
]
