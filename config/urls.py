from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

from cuentas.views import home_view

def landing_page(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('inicio/', home_view, name='home'),
    path('cuentas/', include('cuentas.urls')),
    path('indicadores/', include('indicadores.urls')),
    path('agenda/', include('agenda.urls')),
]
