# Tareas — Sistema de gestión para talleres de escape y mecánica ligera

> Stack: Django 5.x + HTMX + Bootstrap 5 + SQLite → PostgreSQL  
> Objetivo: reducir en >50% el tiempo de cotización y gestión de stock, eliminar el uso de Excel.  
> Ritmo estimado: 1–2 horas diarias · Total: ~7 semanas

---

## Fase 1 — Fundación del proyecto (~1 semana)

- [ ] Crear entorno virtual (`venv`) e instalar Django 5.x
- [ ] Crear proyecto Django (`django-admin startproject`)
- [ ] Inicializar repositorio git y primer commit
- [ ] Configurar SQLite como base de datos de desarrollo
- [ ] Definir estructura de apps: `core`, `catalogo`, `compatibilidades`, `cotizacion`
- [ ] Crear template base con navegación lateral (Bootstrap 5)
- [ ] Implementar login simple con `django.contrib.auth` (un usuario por taller)

**Entregable:** app corriendo en local, login funcionando, estructura de carpetas definida.

---

## Fase 2 — Productos y stock (~2 semanas)

### Modelos
- [ ] `Categoria` — nombre, margen_porcentaje
- [ ] `Producto` — nombre, codigo_interno, tipo (específico/universal), costo, stock_actual, stock_minimo, FK a Categoria
- [ ] `Proveedor` — nombre, contacto
- [ ] `PrecioProveedor` — costo, fecha_actualizacion, FK a Producto y Proveedor
- [ ] Crear y aplicar migraciones

### Vistas y templates
- [ ] CRUD de categorías
- [ ] CRUD de productos con búsqueda por nombre, código y categoría (HTMX)
- [ ] CRUD de proveedores y precios por proveedor
- [ ] Alerta visual cuando el stock baja del mínimo
- [ ] Vista de importación masiva desde CSV

**Entregable:** el taller puede cargar y consultar su catálogo completo sin Excel.

---

## Fase 3 — Precios y márgenes (~1 semana)

- [ ] Cálculo automático del precio de venta según margen de categoría
- [ ] Vista de actualización masiva de precios por categoría (subir % de costo en un clic)
- [ ] Historial de cambios de precio por producto (quién y cuándo)
- [ ] Vista "margen en riesgo": productos con precio de venta muy cerca del costo

**Entregable:** actualizar precios tras un aumento de proveedor toma minutos, no horas.

---

## Fase 4 — Compatibilidades (~1 semana)

- [ ] Modelo `Vehiculo` — marca, modelo, anio
- [ ] Modelo `Compatibilidad` — FK a Producto y Vehículo, campo nota libre
- [ ] CRUD de vehículos
- [ ] CRUD de compatibilidades (carga 100% manual, sin IA)
- [ ] Búsqueda: "¿qué tengo para un Ford Ka 2015?" → lista de piezas compatibles (HTMX)

**Entregable:** un empleado puede responder compatibilidades sin preguntarle al dueño.

---

## Fase 5 — Cotización — núcleo del MVP (~2 semanas)

### Modelos
- [ ] `Presupuesto` — cliente, fecha, estado (borrador/aceptado/rechazado), mano_de_obra, total
- [ ] `ItemPresupuesto` — FK a Presupuesto y Producto, cantidad, precio_unitario, subtotal

### Funciones
- [ ] Buscador de piezas en tiempo real con HTMX mientras se arma el presupuesto
- [ ] Campo libre para mano de obra (ingresado manualmente por el dueño)
- [ ] Cálculo automático del total (repuestos + mano de obra)
- [ ] Cambio de estado: borrador → aceptado → descuento automático de stock
- [ ] Exportar presupuesto a PDF con logo y datos del taller (WeasyPrint)

**Entregable:** flujo completo de punta a punta — el cliente entra y sale con un presupuesto.

---

## Criterios de éxito del MVP

- [ ] Un taller puede cargar su catálogo completo desde cero o importando un CSV
- [ ] Se puede armar un presupuesto completo en menos de 5 minutos
- [ ] Actualizar los precios de una categoría entera toma menos de 2 minutos
- [ ] El stock se descuenta solo al confirmar un trabajo
- [ ] Un empleado nuevo puede encontrar una pieza compatible sin ayuda del dueño

---

## Fuera de scope (v2 o más adelante)

Facturación fiscal · Contabilidad · CRM · Agenda de turnos · Cálculo automático de mano de obra · Diagnóstico mecánico · Multi sucursal · Multi usuario · Cloud/SaaS · App móvil · Integración con proveedores

---

*Última actualización: 2026-05-28 — Fase 1 pendiente de inicio.*
