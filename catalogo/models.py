from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    margen_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"
        ordering = ['nombre']


class Proveedor(models.Model):
    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Proveedores"
        ordering = ['nombre']


class Producto(models.Model):
    TIPO_ESPECIFICO = 'especifico'
    TIPO_UNIVERSAL = 'universal'
    TIPO_CHOICES = [
        (TIPO_ESPECIFICO, 'Específico'),
        (TIPO_UNIVERSAL, 'Universal'),
    ]

    nombre = models.CharField(max_length=200)
    codigo_interno = models.CharField(max_length=50, unique=True)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default=TIPO_ESPECIFICO)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')
    costo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_actual = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)

    @property
    def precio_venta(self):
        return self.costo * (1 + self.categoria.margen_porcentaje / 100)

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo

    def __str__(self):
        return f"{self.codigo_interno} — {self.nombre}"

    class Meta:
        verbose_name_plural = "Productos"
        ordering = ['nombre']


class PrecioProveedor(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='precios_proveedor')
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='precios')
    costo = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_actualizacion = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.proveedor} — {self.producto} — ${self.costo}"

    class Meta:
        verbose_name_plural = "Precios de proveedor"
        unique_together = [['producto', 'proveedor']]
