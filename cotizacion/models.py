from decimal import Decimal
from django.db import models


class Presupuesto(models.Model):
    BORRADOR = 'borrador'
    ACEPTADO = 'aceptado'
    RECHAZADO = 'rechazado'
    ESTADO_CHOICES = [
        (BORRADOR, 'Borrador'),
        (ACEPTADO, 'Aceptado'),
        (RECHAZADO, 'Rechazado'),
    ]

    cliente = models.CharField(max_length=200)
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default=BORRADOR)
    mano_de_obra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def recalcular_total(self):
        subtotal = sum(item.subtotal for item in self.items.all())
        self.total = subtotal + self.mano_de_obra
        self.save(update_fields=['total'])
        return self.total

    def subtotal_items(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"#{self.pk} — {self.cliente} ({self.get_estado_display()})"

    class Meta:
        verbose_name = "Presupuesto"
        verbose_name_plural = "Presupuestos"
        ordering = ['-pk']


class ItemPresupuesto(models.Model):
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey('catalogo.Producto', on_delete=models.PROTECT, related_name='items_presupuesto')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        self.subtotal = self.precio_unitario * Decimal(self.cantidad)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.producto.nombre} x{self.cantidad}"

    class Meta:
        verbose_name = "Ítem de presupuesto"
        verbose_name_plural = "Ítems de presupuesto"
