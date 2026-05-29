from django import forms
from .models import Categoria, PrecioProveedor, Producto, Proveedor

_ctrl = {'class': 'form-control'}
_sel = {'class': 'form-select'}


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'margen_porcentaje']
        widgets = {
            'nombre': forms.TextInput(attrs=_ctrl),
            'margen_porcentaje': forms.NumberInput(attrs={**_ctrl, 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'margen_porcentaje': 'Margen (%)',
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_interno', 'tipo', 'categoria', 'costo', 'stock_actual', 'stock_minimo']
        widgets = {
            'nombre': forms.TextInput(attrs=_ctrl),
            'codigo_interno': forms.TextInput(attrs=_ctrl),
            'tipo': forms.Select(attrs=_sel),
            'categoria': forms.Select(attrs=_sel),
            'costo': forms.NumberInput(attrs={**_ctrl, 'step': '0.01', 'min': '0'}),
            'stock_actual': forms.NumberInput(attrs={**_ctrl, 'min': '0'}),
            'stock_minimo': forms.NumberInput(attrs={**_ctrl, 'min': '0'}),
        }
        labels = {
            'codigo_interno': 'Código interno',
            'costo': 'Costo ($)',
            'stock_actual': 'Stock actual',
            'stock_minimo': 'Stock mínimo',
        }


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto']
        widgets = {
            'nombre': forms.TextInput(attrs=_ctrl),
            'contacto': forms.TextInput(attrs={**_ctrl, 'placeholder': 'Teléfono, email, nombre…'}),
        }


class PrecioProveedorForm(forms.ModelForm):
    class Meta:
        model = PrecioProveedor
        fields = ['proveedor', 'costo']
        widgets = {
            'proveedor': forms.Select(attrs=_sel),
            'costo': forms.NumberInput(attrs={**_ctrl, 'step': '0.01', 'min': '0'}),
        }
        labels = {
            'costo': 'Costo del proveedor ($)',
        }
