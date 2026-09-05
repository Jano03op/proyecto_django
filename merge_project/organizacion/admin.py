from django.contrib import admin

from .models import Cargo, Delegacion, Funcionario


@admin.register(Delegacion)
class DelegacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'n_funcionarios')
    list_filter = ('estado',)
    search_fields = ('nombre', 'ambito')


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cargo', 'delegacion', 'estado', 'es_verificador')
    list_filter = ('delegacion', 'cargo', 'estado', 'es_verificador')
    search_fields = ('nombre',)
