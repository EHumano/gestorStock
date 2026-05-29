from django.contrib import admin
from .models import Categoria, PrecioProveedor, Producto, Proveedor

admin.site.register(Categoria)
admin.site.register(Proveedor)
admin.site.register(PrecioProveedor)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo_interno', 'nombre', 'categoria', 'tipo', 'stock_actual', 'stock_minimo']
    list_filter = ['categoria', 'tipo']
    search_fields = ['nombre', 'codigo_interno']
