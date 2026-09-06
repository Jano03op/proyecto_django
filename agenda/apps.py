from django.apps import AppConfig


class AgendaConfig(AppConfig):
    # Nombre exacto de la carpeta de la app. Django usa este valor para
    # encontrar la app dentro del proyecto y para armar el namespace de
    # las migraciones. Debe coincidir con el nombre agregado en
    # config/settings.py -> INSTALLED_APPS.
    name = 'agenda'
