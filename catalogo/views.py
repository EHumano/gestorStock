import csv
import io
from decimal import Decimal, InvalidOperation

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, PrecioProveedorForm, ProductoForm, ProveedorForm
from .models import Categoria, HistorialPrecio, Producto, Proveedor


# ── Categorías ───────────────────────────────────────────────────────────────

@login_required
def categoria_lista(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/categoria_lista.html', {'categorias': categorias})


@login_required
def categoria_crear(request):
    form = CategoriaForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('catalogo:categoria_lista')
    return render(request, 'catalogo/categoria_form.html', {'form': form, 'titulo': 'Nueva categoría'})


@login_required
def categoria_editar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if form.is_valid():
        form.save()
        messages.success(request, 'Categoría actualizada.')
        return redirect('catalogo:categoria_lista')
    return render(request, 'catalogo/categoria_form.html', {'form': form, 'titulo': 'Editar categoría'})


@login_required
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada.')
        return redirect('catalogo:categoria_lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': categoria,
        'cancelar_url': 'catalogo:categoria_lista',
    })


# ── Productos ────────────────────────────────────────────────────────────────

@login_required
def producto_lista(request):
    categorias = Categoria.objects.all()
    productos = _filtrar_productos(request)
    return render(request, 'catalogo/producto_lista.html', {
        'productos': productos,
        'categorias': categorias,
    })


@login_required
def producto_buscar(request):
    productos = _filtrar_productos(request)
    return render(request, 'catalogo/producto_tabla.html', {'productos': productos})


def _filtrar_productos(request):
    q = request.GET.get('q', '').strip()
    categoria_id = request.GET.get('categoria', '').strip()
    productos = Producto.objects.select_related('categoria').all()
    if q:
        productos = productos.filter(Q(nombre__icontains=q) | Q(codigo_interno__icontains=q))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    return productos


@login_required
def producto_crear(request):
    form = ProductoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Producto creado.')
        return redirect('catalogo:producto_lista')
    return render(request, 'catalogo/producto_form.html', {'form': form, 'titulo': 'Nuevo producto'})


@login_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    costo_anterior = producto.costo
    form = ProductoForm(request.POST or None, instance=producto)
    if form.is_valid():
        guardado = form.save()
        if guardado.costo != costo_anterior:
            HistorialPrecio.objects.create(
                producto=guardado,
                costo_anterior=costo_anterior,
                costo_nuevo=guardado.costo,
                usuario=request.user,
            )
        messages.success(request, 'Producto actualizado.')
        return redirect('catalogo:producto_lista')
    precios = producto.precios_proveedor.select_related('proveedor').all()
    precio_form = PrecioProveedorForm()
    return render(request, 'catalogo/producto_form.html', {
        'form': form,
        'titulo': 'Editar producto',
        'producto': producto,
        'precios': precios,
        'precio_form': precio_form,
    })


@login_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado.')
        return redirect('catalogo:producto_lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': producto,
        'cancelar_url': 'catalogo:producto_lista',
    })


@login_required
def producto_historial(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    historial = producto.historial_precios.select_related('usuario').all()
    return render(request, 'catalogo/producto_historial.html', {
        'producto': producto,
        'historial': historial,
    })


@login_required
def producto_importar_csv(request):
    if request.method == 'POST' and request.FILES.get('archivo'):
        archivo = request.FILES['archivo']
        try:
            texto = archivo.read().decode('utf-8')
        except UnicodeDecodeError:
            texto = archivo.read().decode('latin-1')

        reader = csv.DictReader(io.StringIO(texto))
        creados = actualizados = 0
        errores = []

        for i, fila in enumerate(reader, start=2):
            try:
                nombre_cat = fila.get('categoria', '').strip() or 'Sin categoría'
                categoria, _ = Categoria.objects.get_or_create(
                    nombre=nombre_cat,
                    defaults={'margen_porcentaje': 0},
                )
                tipo = fila.get('tipo', 'especifico').strip().lower()
                if tipo not in ('especifico', 'universal'):
                    tipo = 'especifico'
                _, created = Producto.objects.update_or_create(
                    codigo_interno=fila['codigo_interno'].strip(),
                    defaults={
                        'nombre': fila['nombre'].strip(),
                        'tipo': tipo,
                        'categoria': categoria,
                        'costo': Decimal(fila.get('costo', '0').replace(',', '.')),
                        'stock_actual': int(fila.get('stock_actual', 0)),
                        'stock_minimo': int(fila.get('stock_minimo', 0)),
                    },
                )
                if created:
                    creados += 1
                else:
                    actualizados += 1
            except (KeyError, InvalidOperation, ValueError) as e:
                errores.append(f"Fila {i}: {e}")

        if errores:
            messages.warning(request, f'{creados} creados, {actualizados} actualizados. Errores: {"; ".join(errores[:5])}')
        else:
            messages.success(request, f'{creados} productos creados, {actualizados} actualizados.')
        return redirect('catalogo:producto_lista')

    return render(request, 'catalogo/producto_importar.html')


# ── Precios y márgenes ───────────────────────────────────────────────────────

@login_required
def actualizacion_masiva(request):
    categorias = Categoria.objects.all()
    preview = None

    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        try:
            porcentaje = Decimal(request.POST.get('porcentaje', '0').replace(',', '.'))
        except InvalidOperation:
            messages.error(request, 'Porcentaje inválido.')
            return render(request, 'catalogo/actualizacion_masiva.html', {'categorias': categorias})

        categoria = get_object_or_404(Categoria, pk=categoria_id)
        productos = list(Producto.objects.filter(categoria=categoria))

        if not productos:
            messages.warning(request, f'La categoría "{categoria.nombre}" no tiene productos.')
            return render(request, 'catalogo/actualizacion_masiva.html', {'categorias': categorias})

        factor = 1 + porcentaje / 100
        historial_bulk = []
        for p in productos:
            costo_anterior = p.costo
            p.costo = (p.costo * factor).quantize(Decimal('0.01'))
            historial_bulk.append(HistorialPrecio(
                producto=p,
                costo_anterior=costo_anterior,
                costo_nuevo=p.costo,
                usuario=request.user,
            ))

        Producto.objects.bulk_update(productos, ['costo'])
        HistorialPrecio.objects.bulk_create(historial_bulk)

        signo = '+' if porcentaje >= 0 else ''
        messages.success(
            request,
            f'{len(productos)} productos de "{categoria.nombre}" actualizados ({signo}{porcentaje}%).'
        )
        return redirect('catalogo:actualizacion_masiva')

    # Vista previa HTMX al cambiar categoría
    categoria_id = request.GET.get('categoria')
    if categoria_id:
        try:
            cat = Categoria.objects.get(pk=categoria_id)
            preview = cat.productos.all()
        except Categoria.DoesNotExist:
            pass

    return render(request, 'catalogo/actualizacion_masiva.html', {
        'categorias': categorias,
        'preview': preview,
    })


@login_required
def margen_riesgo(request):
    try:
        umbral = Decimal(request.GET.get('umbral', '20'))
    except InvalidOperation:
        umbral = Decimal('20')

    productos = (
        Producto.objects
        .select_related('categoria')
        .filter(categoria__margen_porcentaje__lt=umbral)
        .order_by('categoria__margen_porcentaje', 'nombre')
    )
    return render(request, 'catalogo/margen_riesgo.html', {
        'productos': productos,
        'umbral': umbral,
    })


# ── Proveedores ──────────────────────────────────────────────────────────────

@login_required
def proveedor_lista(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'catalogo/proveedor_lista.html', {'proveedores': proveedores})


@login_required
def proveedor_crear(request):
    form = ProveedorForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proveedor creado.')
        return redirect('catalogo:proveedor_lista')
    return render(request, 'catalogo/proveedor_form.html', {'form': form, 'titulo': 'Nuevo proveedor'})


@login_required
def proveedor_editar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    form = ProveedorForm(request.POST or None, instance=proveedor)
    if form.is_valid():
        form.save()
        messages.success(request, 'Proveedor actualizado.')
        return redirect('catalogo:proveedor_lista')
    return render(request, 'catalogo/proveedor_form.html', {'form': form, 'titulo': 'Editar proveedor'})


@login_required
def proveedor_eliminar(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado.')
        return redirect('catalogo:proveedor_lista')
    return render(request, 'catalogo/confirm_delete.html', {
        'objeto': proveedor,
        'cancelar_url': 'catalogo:proveedor_lista',
    })
