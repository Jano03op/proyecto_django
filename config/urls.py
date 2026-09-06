from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing_page'),
    path('indicadores/', include('indicadores.urls')),
    path('agenda/', include('agenda.urls')),
]
