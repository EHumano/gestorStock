from django.urls import path
from . import views

app_name = 'cotizacion'

urlpatterns = [
    path('', views.presupuesto_lista, name='lista'),
    path('nuevo/', views.presupuesto_crear, name='crear'),
    path('<int:pk>/editar/', views.presupuesto_editar, name='editar'),
    path('<int:pk>/eliminar/', views.presupuesto_eliminar, name='eliminar'),
    path('<int:pk>/aceptar/', views.presupuesto_aceptar, name='aceptar'),
    path('<int:pk>/rechazar/', views.presupuesto_rechazar, name='rechazar'),
    path('<int:pk>/pdf/', views.presupuesto_pdf, name='pdf'),

    # HTMX endpoints
    path('<int:pk>/buscar-productos/', views.buscar_productos_htmx, name='buscar_productos'),
    path('<int:pk>/agregar-item/', views.agregar_item_htmx, name='agregar_item'),
    path('<int:pk>/items/<int:item_pk>/eliminar/', views.eliminar_item_htmx, name='eliminar_item'),
    path('<int:pk>/mano-de-obra/', views.actualizar_mano_obra_htmx, name='mano_de_obra'),
]
