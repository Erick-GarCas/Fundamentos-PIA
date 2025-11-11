"""
WSGI config for crud_project project.

Este archivo expone la aplicación WSGI en la variable `application`.
El servidor WSGI (por ejemplo Gunicorn o uWSGI en despliegue) importará
esta variable para servir las peticiones HTTP.

Si necesita soporte asíncrono o WebSockets, use `asgi.py` en su lugar.
"""

import os

from django.core.wsgi import get_wsgi_application

# Asegura que Django carga la configuración correcta antes de crear la app
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_project.settings')

# Objeto WSGI que el servidor usará para manejar requests sincrónicas
application = get_wsgi_application()
