from django.urls import path
from . import views

urlpatterns = [
    path('panel/', views.panel_admin, name='panel_admin'),
    path('mis-actividades/', views.panel_funcionario, name='panel_funcionario'),
    path('registrar/', views.registrar_actividad, name='registrar_actividad'),
    path('validar/<int:id>/', views.validar_evidencia, name='validar_evidencia'),
]
