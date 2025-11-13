"""
Configuración de la aplicación `app`.

Este módulo define la clase `AppConfig` que Django utiliza para registrar
la aplicación dentro del proyecto. Aquí se documentan las responsabilidades
comunes y recomendaciones para desarrolladores que mantendrán esta app.

Resumen de responsabilidades:
- `default_auto_field`: tipo de campo por defecto para nuevos modelos.
- `name`: nombre importable de la aplicación, usado por Django para localizarla.
- `ready()`: método opcional para inicializaciones ligeras (registro de señales,
    hooks de métricas, etc.). Evitar lógica costosa en `ready()`.

Buenas prácticas:
- Registrar señales dentro de `ready()` usando importaciones locales para evitar
    importaciones circulares durante el arranque.
- No ejecutar I/O o tareas pesadas en `ready()`; preferir tareas asíncronas o
    jobs programados.

Ejemplo breve (registro de señales):
        def ready(self):
                # from . import signals  # importación local a prueba de ciclos
                # signals.register_handlers()
                pass

"""

from django.apps import AppConfig as _AppConfig


class AppConfig(_AppConfig):
        # DEFAULT_AUTO_FIELD: define el tipo de campo que se usará por defecto
        # para los nuevos modelos creados en esta aplicación. Se utiliza
        # 'BigAutoField' para permitir un rango amplio de valores en las PKs.
        default_auto_field = 'django.db.models.BigAutoField'

        # NAME: nombre del paquete que Django utiliza para encontrar la app.
        # Debe coincidir con la ruta del paquete (p. ej. 'app' si el paquete está
        # en `crud_project/app`). Cambiar solo si se mueve o renombra el paquete.
        name = 'app'

        # Método opcional que Django llama cuando la app está lista.
        # Úsalo para registrar señales o inicializaciones ligeras.
        # Evita operaciones lentas o bloqueantes aquí para no retrasar el arranque.
        def ready(self):
                # Ejemplo (comentado): registrar señales con importación local
                # from . import signals
                # signals.connect_handlers()
                pass
