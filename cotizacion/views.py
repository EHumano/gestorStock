from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from catalogo.models import Producto
from core.models import TallerConfig
from .forms import ManoDeObraForm, PresupuestoForm
from .models import ItemPresupuesto, Presupuesto


# ── Lista ─────────────────────────────────────────────────────────────────────

@login_required
def presupuesto_lista(request):
    estado = request.GET.get('estado', '')
    presupuestos = Presupuesto.objects.all()
    if estado:
        presupuestos = presupuestos.filter(estado=estado)
    return render(request, 'cotizacion/lista.html', {
        'presupuestos': presupuestos,
        'estado_filtro': estado,
        'estados': Presupuesto.ESTADO_CHOICES,
    })


# ── Crear ─────────────────────────────────────────────────────────────────────

@login_required
def presupuesto_crear(request):
    form = PresupuestoForm(request.POST or None)
    if form.is_valid():
        presupuesto = form.save()
        return redirect('cotizacion:editar', pk=presupuesto.pk)
    return render(request, 'cotizacion/presupuesto_crear.html', {'form': form})


# ── Editar ────────────────────────────────────────────────────────────────────

@login_required
def presupuesto_editar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    items = presupuesto.items.select_related('producto__categoria').all()
    mano_form = ManoDeObraForm(instance=presupuesto)
    return render(request, 'cotizacion/presupuesto_editar.html', {
        'presupuesto': presupuesto,
        'items': items,
        'mano_form': mano_form,
    })


# ── Eliminar ──────────────────────────────────────────────────────────────────

@login_required
def presupuesto_eliminar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method == 'POST':
        presupuesto.delete()
        messages.success(request, 'Presupuesto eliminado.')
        return redirect('cotizacion:lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': presupuesto,
        'cancelar_url': 'cotizacion:lista',
    })


# ── Cambios de estado ─────────────────────────────────────────────────────────

@login_required
def presupuesto_aceptar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method != 'POST':
        return redirect('cotizacion:editar', pk=pk)

    if presupuesto.estado == Presupuesto.ACEPTADO:
        messages.warning(request, 'El presupuesto ya fue aceptado.')
        return redirect('cotizacion:editar', pk=pk)

    items = presupuesto.items.select_related('producto').all()
    if not items.exists():
        messages.error(request, 'El presupuesto no tiene ítems.')
        return redirect('cotizacion:editar', pk=pk)

    # Verificar stock suficiente
    sin_stock = []
    for item in items:
        if item.producto.stock_actual < item.cantidad:
            sin_stock.append(f"{item.producto.nombre} (stock: {item.producto.stock_actual}, necesario: {item.cantidad})")
    if sin_stock:
        messages.error(request, 'Stock insuficiente: ' + ' | '.join(sin_stock))
        return redirect('cotizacion:editar', pk=pk)

    # Descontar stock
    for item in items:
        item.producto.stock_actual -= item.cantidad
        item.producto.save(update_fields=['stock_actual'])

    presupuesto.estado = Presupuesto.ACEPTADO
    presupuesto.save(update_fields=['estado'])
    messages.success(request, f'Presupuesto #{presupuesto.pk} aceptado. Stock descontado.')
    return redirect('cotizacion:editar', pk=pk)


@login_required
def presupuesto_rechazar(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if request.method == 'POST':
        presupuesto.estado = Presupuesto.RECHAZADO
        presupuesto.save(update_fields=['estado'])
        messages.info(request, f'Presupuesto #{presupuesto.pk} marcado como rechazado.')
    return redirect('cotizacion:editar', pk=pk)


# ── PDF ───────────────────────────────────────────────────────────────────────

@login_required
def presupuesto_pdf(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    items = presupuesto.items.select_related('producto').all()
    config = TallerConfig.get()

    html = render_to_string('cotizacion/presupuesto_pdf.html', {
        'presupuesto': presupuesto,
        'items': items,
        'config': config,
    }, request=request)

    from weasyprint import HTML
    pdf = HTML(string=html, base_url=request.build_absolute_uri('/')).write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="presupuesto_{presupuesto.pk}.pdf"'
    return response


# ── HTMX: búsqueda de productos ───────────────────────────────────────────────

@login_required
def buscar_productos_htmx(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    q = request.GET.get('q', '').strip()
    productos = []
    if q:
        ya_en_presupuesto = presupuesto.items.values_list('producto_id', flat=True)
        productos = (
            Producto.objects
            .select_related('categoria')
            .filter(Q(nombre__icontains=q) | Q(codigo_interno__icontains=q))
            .exclude(pk__in=ya_en_presupuesto)[:10]
        )
    return render(request, 'cotizacion/productos_busqueda.html', {
        'productos': productos,
        'presupuesto': presupuesto,
        'q': q,
    })


# ── HTMX: agregar ítem ────────────────────────────────────────────────────────

@login_required
def agregar_item_htmx(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if presupuesto.estado != Presupuesto.BORRADOR:
        return _items_response(request, presupuesto)

    producto_id = request.POST.get('producto_id')
    try:
        cantidad = max(1, int(request.POST.get('cantidad', 1)))
    except (ValueError, TypeError):
        cantidad = 1

    producto = get_object_or_404(Producto, pk=producto_id)

    item, created = ItemPresupuesto.objects.get_or_create(
        presupuesto=presupuesto,
        producto=producto,
        defaults={'precio_unitario': producto.precio_venta, 'cantidad': cantidad},
    )
    if not created:
        item.cantidad += cantidad
        item.save()

    presupuesto.recalcular_total()
    return _items_response(request, presupuesto)


# ── HTMX: eliminar ítem ───────────────────────────────────────────────────────

@login_required
def eliminar_item_htmx(request, pk, item_pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if presupuesto.estado == Presupuesto.BORRADOR:
        ItemPresupuesto.objects.filter(pk=item_pk, presupuesto=presupuesto).delete()
        presupuesto.recalcular_total()
    return _items_response(request, presupuesto)


# ── HTMX: mano de obra ────────────────────────────────────────────────────────

@login_required
def actualizar_mano_obra_htmx(request, pk):
    presupuesto = get_object_or_404(Presupuesto, pk=pk)
    if presupuesto.estado == Presupuesto.BORRADOR:
        try:
            valor = Decimal(request.POST.get('mano_de_obra', '0').replace(',', '.'))
            presupuesto.mano_de_obra = max(Decimal('0'), valor)
            presupuesto.save(update_fields=['mano_de_obra'])
            presupuesto.recalcular_total()
        except InvalidOperation:
            pass
    return render(request, 'cotizacion/resumen_parcial.html', {'presupuesto': presupuesto})


# ── Helper ────────────────────────────────────────────────────────────────────

def _items_response(request, presupuesto):
    items = presupuesto.items.select_related('producto__categoria').all()
    return render(request, 'cotizacion/items_parcial.html', {
        'presupuesto': presupuesto,
        'items': items,
    })
