from django.db import models


class Vehiculo(models.Model):
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    anio = models.PositiveSmallIntegerField(verbose_name="Año")

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio}"

    class Meta:
        verbose_name = "Vehículo"
        verbose_name_plural = "Vehículos"
        ordering = ['marca', 'modelo', 'anio']
        unique_together = [['marca', 'modelo', 'anio']]


class Compatibilidad(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='compatibilidades')
    producto = models.ForeignKey('catalogo.Producto', on_delete=models.CASCADE, related_name='compatibilidades')
    nota = models.CharField(max_length=300, blank=True, help_text='Ej: "sirve adaptando soporte"')

    def __str__(self):
        return f"{self.vehiculo} ↔ {self.producto}"

    class Meta:
        verbose_name_plural = "Compatibilidades"
        unique_together = [['vehiculo', 'producto']]
