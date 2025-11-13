#!/usr/bin/env python
# Pequeño envoltorio CLI utilizado por proyectos Django.
#
# Este archivo crea la entrada de línea de comandos del proyecto Django
# y expone la función `main()` que configura `DJANGO_SETTINGS_MODULE`
# y delega a la utilidad de Django para ejecutar comandos como:
# - `python manage.py migrate`       -> aplica migraciones de base de datos
# - `python manage.py runserver`     -> inicia el servidor de desarrollo
# - `python manage.py createsuperuser` -> crea un usuario administrador
#
# No contiene lógica de negocio; su objetivo es inicializar y arrancar
# la utilidad de gestión de Django.

import os
import sys


def main():
    # Configura la variable de entorno que indica qué archivo de settings
    # debe usar Django. Aquí apuntamos a `crud_project.settings`.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crud_project.settings')

    try:
        # Import tardío de la función que procesa los comandos pasados por CLI.
        # Se hace aquí para que, si falta Django, el error sea más claro.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si Django no está instalado o no se activó el entorno virtual,
        # lanzamos un ImportError informativo. En clase basta con saber
        # que este error indica que falta la librería Django en el entorno.
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # `execute_from_command_line` interpreta `sys.argv` y ejecuta el comando.
    # Ejemplos útiles para práctica escolar:
    #   - python manage.py runserver
    #   - python manage.py makemigrations
    #   - python manage.py migrate
    #   - python manage.py createsuperuser
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
