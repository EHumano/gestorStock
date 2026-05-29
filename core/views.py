from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import TallerConfig


@login_required
def inicio(request):
    return render(request, 'inicio.html')


class TallerConfigForm(forms.ModelForm):
    class Meta:
        model = TallerConfig
        fields = ['nombre', 'domicilio', 'telefono', 'email']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }


@login_required
def taller_config(request):
    config = TallerConfig.get()
    form = TallerConfigForm(request.POST or None, instance=config)
    if form.is_valid():
        form.save()
        messages.success(request, 'Configuración guardada.')
        return redirect('configuracion')
    return render(request, 'core/configuracion.html', {'form': form})
