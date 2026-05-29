from django.contrib import admin
from .models import Compatibilidad, Vehiculo


@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['marca', 'modelo', 'anio']
    search_fields = ['marca', 'modelo']
    list_filter = ['marca']


@admin.register(Compatibilidad)
class CompatibilidadAdmin(admin.ModelAdmin):
    list_display = ['vehiculo', 'producto', 'nota']
    search_fields = ['vehiculo__marca', 'vehiculo__modelo', 'producto__nombre']
