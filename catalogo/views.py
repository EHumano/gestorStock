from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def producto_lista(request):
    return render(request, 'catalogo/producto_lista.html')


@login_required
def categoria_lista(request):
    return render(request, 'catalogo/categoria_lista.html')


@login_required
def proveedor_lista(request):
    return render(request, 'catalogo/proveedor_lista.html')
