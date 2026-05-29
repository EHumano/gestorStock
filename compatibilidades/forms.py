from django import forms
from .models import Compatibilidad, Vehiculo

_ctrl = {'class': 'form-control'}
_sel = {'class': 'form-select'}


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['marca', 'modelo', 'anio']
        widgets = {
            'marca': forms.TextInput(attrs={**_ctrl, 'placeholder': 'Ej: Ford'}),
            'modelo': forms.TextInput(attrs={**_ctrl, 'placeholder': 'Ej: Ka'}),
            'anio': forms.NumberInput(attrs={**_ctrl, 'min': 1950, 'max': 2100}),
        }
        labels = {'anio': 'Año'}


class CompatibilidadForm(forms.ModelForm):
    class Meta:
        model = Compatibilidad
        fields = ['vehiculo', 'producto', 'nota']
        widgets = {
            'vehiculo': forms.Select(attrs=_sel),
            'producto': forms.Select(attrs=_sel),
            'nota': forms.TextInput(attrs={**_ctrl, 'placeholder': 'Ej: sirve adaptando soporte (opcional)'}),
        }
