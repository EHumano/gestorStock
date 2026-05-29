from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CompatibilidadForm, VehiculoForm
from .models import Compatibilidad, Vehiculo


# ── Búsqueda ─────────────────────────────────────────────────────────────────

@login_required
def compatibilidad_lista(request):
    return render(request, 'compatibilidades/lista.html')


@login_required
def compatibilidad_buscar(request):
    marca = request.GET.get('marca', '').strip()
    modelo = request.GET.get('modelo', '').strip()
    anio = request.GET.get('anio', '').strip()

    vehiculos = None
    if marca or modelo or anio:
        vehiculos = Vehiculo.objects.prefetch_related(
            'compatibilidades__producto__categoria'
        ).all()
        if marca:
            vehiculos = vehiculos.filter(marca__icontains=marca)
        if modelo:
            vehiculos = vehiculos.filter(modelo__icontains=modelo)
        if anio:
            try:
                vehiculos = vehiculos.filter(anio=int(anio))
            except ValueError:
                pass

    return render(request, 'compatibilidades/resultados.html', {'vehiculos': vehiculos})


# ── Compatibilidades ──────────────────────────────────────────────────────────

@login_required
def compatibilidad_crear(request):
    vehiculo_id = request.GET.get('vehiculo')
    initial = {'vehiculo': vehiculo_id} if vehiculo_id else {}
    form = CompatibilidadForm(request.POST or None, initial=initial)
    if form.is_valid():
        form.save()
        messages.success(request, 'Compatibilidad agregada.')
        return redirect('compatibilidades:lista')
    return render(request, 'compatibilidades/compatibilidad_form.html', {
        'form': form,
        'titulo': 'Nueva compatibilidad',
    })


@login_required
def compatibilidad_eliminar(request, pk):
    comp = get_object_or_404(Compatibilidad, pk=pk)
    if request.method == 'POST':
        comp.delete()
        messages.success(request, 'Compatibilidad eliminada.')
        return redirect('compatibilidades:lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': comp,
        'cancelar_url': 'compatibilidades:lista',
    })


# ── Vehículos ─────────────────────────────────────────────────────────────────

@login_required
def vehiculo_lista(request):
    q = request.GET.get('q', '').strip()
    vehiculos = Vehiculo.objects.all()
    if q:
        vehiculos = vehiculos.filter(
            Q(marca__icontains=q) | Q(modelo__icontains=q)
        )
    return render(request, 'compatibilidades/vehiculo_lista.html', {
        'vehiculos': vehiculos,
        'q': q,
    })


@login_required
def vehiculo_crear(request):
    form = VehiculoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Vehículo creado.')
        return redirect('compatibilidades:vehiculo_lista')
    return render(request, 'compatibilidades/vehiculo_form.html', {
        'form': form,
        'titulo': 'Nuevo vehículo',
    })


@login_required
def vehiculo_editar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    form = VehiculoForm(request.POST or None, instance=vehiculo)
    if form.is_valid():
        form.save()
        messages.success(request, 'Vehículo actualizado.')
        return redirect('compatibilidades:vehiculo_lista')
    return render(request, 'compatibilidades/vehiculo_form.html', {
        'form': form,
        'titulo': 'Editar vehículo',
    })


@login_required
def vehiculo_eliminar(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        messages.success(request, 'Vehículo eliminado.')
        return redirect('compatibilidades:vehiculo_lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': vehiculo,
        'cancelar_url': 'compatibilidades:vehiculo_lista',
    })
