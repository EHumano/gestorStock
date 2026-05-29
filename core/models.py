from django.db import models


class TallerConfig(models.Model):
    nombre = models.CharField(max_length=200, default='Mi Taller')
    domicilio = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Configuración del taller"
        verbose_name_plural = "Configuración del taller"
