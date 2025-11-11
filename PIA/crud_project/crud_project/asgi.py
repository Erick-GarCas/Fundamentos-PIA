"""
ASGI config for crud_project project.

Este módulo expone la variable de nivel de módulo `application`, que
es el punto de entrada compatible con ASGI (servidores asíncronos).

Notas breves:
 - ASGI (Asynchronous Server Gateway Interface) es la especificación
	 para comunicaciones asíncronas en Python (WebSockets, HTTP2, etc.).
 - Django la ofrece por compatibilidad con servidores asíncronos; si
	 no se usa funcionalidad asíncrona, el comportamiento es equivalente
	 al de WSGI para HTTP tradicional.
"""

import os

from django.core.asgi import get_asgi_application

# Asegura que Django carga el módulo de settings correcto antes de
# instanciar la aplicación ASGI.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_project.settings')

# Crea la aplicación ASGI que el servidor utilizará para servir
# peticiones. No hay lógica adicional aquí: se delega en Django.
application = get_asgi_application()
