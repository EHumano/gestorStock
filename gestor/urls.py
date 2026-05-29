from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', core_views.inicio, name='inicio'),
    path('catalogo/', include('catalogo.urls')),
    path('compatibilidades/', include('compatibilidades.urls')),
    path('cotizacion/', include('cotizacion.urls')),
]
