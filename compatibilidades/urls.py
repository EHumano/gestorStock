from django.urls import path
from . import views

app_name = 'compatibilidades'

urlpatterns = [
    # Búsqueda principal
    path('', views.compatibilidad_lista, name='lista'),
    path('buscar/', views.compatibilidad_buscar, name='buscar'),

    # CRUD compatibilidades
    path('nueva/', views.compatibilidad_crear, name='crear'),
    path('<int:pk>/eliminar/', views.compatibilidad_eliminar, name='eliminar'),

    # CRUD vehículos
    path('vehiculos/', views.vehiculo_lista, name='vehiculo_lista'),
    path('vehiculos/nuevo/', views.vehiculo_crear, name='vehiculo_crear'),
    path('vehiculos/<int:pk>/editar/', views.vehiculo_editar, name='vehiculo_editar'),
    path('vehiculos/<int:pk>/eliminar/', views.vehiculo_eliminar, name='vehiculo_eliminar'),
]
