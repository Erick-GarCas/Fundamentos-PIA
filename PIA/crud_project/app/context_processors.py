"""
Context processors para plantillas.

Los context processors son funciones que reciben el request y devuelven
un diccionario de variables que estarán disponibles en todas las
plantillas (cuando se declaren en TEMPLATES OPTIONS). Aquí exponemos
banderas de rol para simplificar lógica UI en los templates.
"""


def user_roles(request):
    """Context processor que añade banderas de rol para plantillas.

    Devuelve:
    - is_admin: True si el usuario es superuser o pertenece al grupo 'Administrador'
    - is_employee: True si pertenece al grupo 'Empleado'
    - can_view_citas: True si puede entrar al módulo de citas
    - can_manage_tratamientos: True si puede entrar al módulo de tratamientos
    """
    flags = {
        'is_admin': False,
        'is_employee': False,
        'can_view_citas': False,
        'can_manage_tratamientos': False,
    }
    user = getattr(request, 'user', None)
    try:
        if user and user.is_authenticated:
            is_admin = user.is_superuser or user.groups.filter(name='Administrador').exists()
            flags['is_admin'] = is_admin
            flags['is_employee'] = user.groups.filter(name='Empleado').exists()
            flags['can_view_citas'] = is_admin or user.groups.filter(name='Permiso Citas').exists()
            flags['can_manage_tratamientos'] = is_admin or user.groups.filter(name='Permiso Tratamientos').exists()
    except Exception:
        pass
    return flags
