from django.urls import path
from . import views

app_name = 'cotizacion'

urlpatterns = [
    path('', views.presupuesto_lista, name='lista'),
]
