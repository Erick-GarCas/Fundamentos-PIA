"""
Context processors para plantillas.

Descripción:
- Los context processors son funciones que reciben el `request` y devuelven
  un diccionario de variables que estarán disponibles en todas las
  plantillas si se registran en `TEMPLATES` -> `OPTIONS` -> `context_processors`
  dentro de `settings.py`.
- Este módulo expone `user_roles`, que simplifica la lógica de la interfaz
  mostrando/ocultando elementos según los permisos o grupos del usuario.

Consideraciones de rendimiento y buenas prácticas:
- Evitar consultas costosas o lógica pesada aquí: el context processor se
  ejecuta en cada render de plantilla que use el motor de templates.
- Si necesitas realizar múltiples consultas, considera cachear el resultado
  en `request` (p. ej. `request._roles_cache`) o usar un sistema de cache
  (memcached/redis) para no golpear la DB en cada petición.
- Evitar excepciones silenciosas; aquí la función captura excepciones leves
  para no romper el render, pero en producción es mejor registrar el error.

Ejemplo de registro en `settings.py` (TEMPLATES):

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [...],
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'app.context_processors.user_roles',  # <-- agregar aquí
                ],
            },
        },
    ]

Ejemplo de uso en plantilla (Django template):

    {% if is_admin %}
      <a href="/admin/">Panel de administración</a>
    {% endif %}

"""


def user_roles(request):
    """Context processor que añade banderas de rol para plantillas.

    Retorna un diccionario con banderas booleanas usadas por los templates
    para mostrar/ocultar secciones de la UI.

    Claves devueltas:
    - `is_admin`: True si el usuario es `superuser` o pertenece al grupo 'Administrador'.
    - `is_employee`: True si pertenece al grupo 'Empleado'.
    - `can_view_citas`: True si puede ver el módulo de citas (administrador o grupo 'Permiso Citas').
    - `can_manage_tratamientos`: True si puede gestionar tratamientos (administrador o grupo 'Permiso Tratamientos').

    Nota: la función intenta ser resiliente ante errores y devuelve todas las
    banderas en `False` si algo sale mal, para no interrumpir el render.
    En entornos productivos se recomienda registrar fallos en lugar de silenciarlos.
    """
    flags = {
        'is_admin': False,
        'is_employee': False,
        'can_view_citas': False,
        'can_manage_tratamientos': False,
    }

    # Obtener usuario de la request; puede no existir en contextos puntuales.
    user = getattr(request, 'user', None)

    try:
        # Verificar que el usuario esté autenticado antes de consultar grupos.
        if user and user.is_authenticated:
            # is_admin combina superuser y pertenencia al grupo 'Administrador'.
            is_admin = (
                user.is_superuser
                or user.groups.filter(name='Administrador').exists()
            )
            flags['is_admin'] = is_admin

            # Banderas simples basadas en pertenencia a grupos.
            flags['is_employee'] = user.groups.filter(name='Empleado').exists()
            flags['can_view_citas'] = (
                is_admin or user.groups.filter(name='Permiso Citas').exists()
            )
            flags['can_manage_tratamientos'] = (
                is_admin or user.groups.filter(name='Permiso Tratamientos').exists()
            )
    except Exception:
        # En este contexto preferimos no romper el render de la plantilla.
        # Recomendación: cambiar a logging.exception(...) en producción.
        pass

    return flags
