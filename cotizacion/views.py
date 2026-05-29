from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def presupuesto_lista(request):
    return render(request, 'cotizacion/lista.html')
