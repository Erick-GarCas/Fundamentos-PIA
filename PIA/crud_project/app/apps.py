"""
Configuración de la aplicación `app`.

Contiene la clase AppConfig que Django usa para registrar la app dentro
del proyecto. Aquí se define el tipo de primary key por defecto y el
nombre del paquete.
"""

from django.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
    # DEFAULT_AUTO_FIELD: define el tipo de campo que se usará por defecto
    # para los nuevos modelos creados en esta aplicación.
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
