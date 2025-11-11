"""
Rutas (URLs) de la aplicación `app`.

Define los endpoints que exponen las vistas del panel administrativo y
las páginas públicas de la landing (index, cotizador, solicitud de cita).
Cada `path()` asocia una URL con una función view en `views.py`.
"""

from django.urls import path
from . import views


urlpatterns = [
    # Ruta raíz: muestra la landing
    path('', views.index, name='home'),
    # Listado (template creado por el usuario)
    path('listar/', views.listar, name='listar'),
    # Rutas CRUD mínimas para que los enlaces de la plantilla funcionen
    path('crear/', views.crear, name='crear'),
    path('editar/<int:id>/', views.editar, name='editar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    # Rutas para Citas (CRUD)
    path('citas/', views.citas_listar, name='citas_listar'),
    path('citas/crear/', views.citas_crear, name='citas_crear'),
    path('citas/editar/<int:id>/', views.citas_editar, name='citas_editar'),
    path('citas/eliminar/<int:id>/', views.citas_eliminar, name='citas_eliminar'),
    path('citas/listo/<int:id>/', views.citas_marcar_listo, name='citas_marcar_listo'),
    # Tratamientos
    path('tratamientos/', views.tratamientos_listar, name='tratamientos_listar'),
    path('tratamientos/crear/', views.tratamientos_crear, name='tratamientos_crear'),
    path('tratamientos/editar/<int:id>/', views.tratamientos_editar, name='tratamientos_editar'),
    path('tratamientos/eliminar/<int:id>/', views.tratamientos_eliminar, name='tratamientos_eliminar'),
    # Rutas para Reservaciones (CRUD)
    path('reservaciones/', views.reservaciones_listar, name='reservaciones_listar'),
    path('reservaciones/crear/', views.reservaciones_crear, name='reservaciones_crear'),
    path('reservaciones/editar/<int:id>/', views.reservaciones_editar, name='reservaciones_editar'),
    path('reservaciones/eliminar/<int:id>/', views.reservaciones_eliminar, name='reservaciones_eliminar'),
    path('reservaciones/listo/<int:id>/', views.reservaciones_marcar_listo, name='reservaciones_marcar_listo'),
    # Rutas para gestión de Usuarios (solo administradores)
    path('usuarios/', views.usuarios_listar, name='usuarios_listar'),
    path('usuarios/crear/', views.usuarios_crear, name='usuarios_crear'),
    path('usuarios/editar/<int:id>/', views.usuarios_editar, name='usuarios_editar'),
    path('usuarios/eliminar/<int:id>/', views.usuarios_eliminar, name='usuarios_eliminar'),
    # Solicitar cita (form tradicional POST)
    path('solicitar-cita/', views.solicitar_cita, name='solicitar_cita'),
    # API: lista de tratamientos (JSON)
    path('api/tratamientos/', views.tratamientos_json, name='api_tratamientos'),
    # Registro de usuario (signup)
    path('accounts/signup/', views.signup, name='signup'),

    # Rutas ejemplo para CRUD que desarrollaremos después (seguir tu ejemplo)
    # path('listar/', views.listar_productos, name='listar'),
    # path('crear/', views.crear_producto, name='crear'),
    # path('editar/<int:id>/', views.editar_producto, name='editar'),
    # path('eliminar/<int:id>/', views.eliminar_producto, name='eliminar'),
]
