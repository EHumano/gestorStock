from django import forms
from .models import Presupuesto

_ctrl = {'class': 'form-control'}


class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['cliente']
        widgets = {
            'cliente': forms.TextInput(attrs={**_ctrl, 'placeholder': 'Nombre del cliente', 'autofocus': True}),
        }


class ManoDeObraForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = ['mano_de_obra']
        widgets = {
            'mano_de_obra': forms.NumberInput(attrs={**_ctrl, 'step': '0.01', 'min': '0'}),
        }
        labels = {'mano_de_obra': 'Mano de obra ($)'}
