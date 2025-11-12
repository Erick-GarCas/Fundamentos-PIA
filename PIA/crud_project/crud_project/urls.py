"""
Ruteo principal del proyecto.

Este módulo define `urlpatterns`, la lista que asocia rutas URL con
vistas o a otros módulos de ruteo. Aquí se enlazan el admin, las
URLs de autenticación proporcionadas por Django y las rutas de la app.
"""

from django.contrib import admin
from django.urls import path, include
from app import views as app_views


# Lista principal de rutas. Django las evalúa en orden y ejecuta la
# primera que coincide con la petición.
urlpatterns = [
    # Panel de administración integrado de Django
    path('admin/', admin.site.urls),

    # Rutas de autenticación (login, logout, password reset...) que
    # Django proporciona en 'django.contrib.auth.urls'. Se usan en
    # plantillas y views prefabricadas.
    path('accounts/login/', app_views.login_view, name='login'),
    path('accounts/', include('django.contrib.auth.urls')),

    # Incluye las rutas definidas en la aplicación local `app`.
    # Al usar path('', include('app.urls')) la raíz del sitio
    # se delega a ese módulo de URL.
    path('', include('app.urls')),
]
