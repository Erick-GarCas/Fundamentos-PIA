#!/usr/bin/env python
"""
Small CLI wrapper used by Django projects.

Este archivo crea la entrada de línea de comandos del proyecto Django.
Expone la función `main()` que configura la variable de entorno
`DJANGO_SETTINGS_MODULE` y delega en la utilidad de Django para
ejecutar comandos (migrate, runserver, createsuperuser, etc.).

No contiene lógica de negocio: solo enciende y arranca la interfaz
de comandos provista por Django.
"""

import os
import sys


def main():
    """Configura el entorno y ejecuta la utilidad de gestión de Django.

    Pasos clave:
    - os.environ.setdefault: asegura que Django sabe qué módulo de
      configuración usar (aquí 'crud_project.settings').
    - execute_from_command_line: función de Django que interpreta
      sys.argv y ejecuta el comando solicitado (por ejemplo 'runserver').
    """
    # Indica a Django qué settings usar si no se ha definido externamente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_project.settings')
    try:
        # Ejecuta la utilidad de gestión (import tardío para mejorar
        # tiempos de import y permitir mensajes de error más claros).
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Mensaje explicativo si Django no está instalado o no se activó
        # el entorno virtual; no cambia el comportamiento, solo clarifica.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Delegamos el resto a Django (ej.: manage.py migrate, runserver...)
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
