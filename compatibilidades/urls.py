from django.urls import path
from . import views

app_name = 'compatibilidades'

urlpatterns = [
    path('', views.compatibilidad_lista, name='lista'),
]
