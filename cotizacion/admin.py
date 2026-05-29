from django.contrib import admin
from .models import ItemPresupuesto, Presupuesto


class ItemInline(admin.TabularInline):
    model = ItemPresupuesto
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ['pk', 'cliente', 'fecha', 'estado', 'total']
    list_filter = ['estado', 'fecha']
    search_fields = ['cliente']
    inlines = [ItemInline]
