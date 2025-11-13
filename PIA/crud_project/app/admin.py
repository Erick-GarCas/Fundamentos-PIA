"""
Registro de modelos en el panel de administración de Django.

Aquí simplemente registramos los modelos para que aparezcan en el
admin site. No hay configuraciones personalizadas (ModelAdmin)
porque el proyecto usa las vistas y plantillas propias para CRUD.
"""

from django.contrib import admin
from .models import Tratamiento, CitaDental, Usuario, Reservacion


# Registrar modelos para que sean gestionables desde /admin/
# Si en el futuro quieres personalizar columnas o búsquedas, crea una
# clase ModelAdmin y pásala como segundo argumento a admin.site.register().
admin.site.register(Tratamiento)
admin.site.register(CitaDental)
admin.site.register(Usuario)
admin.site.register(Reservacion)

# -----------------------------------------------
# Manual de uso y guía rápida (comentarios en español)
# -----------------------------------------------
# Qué hace este archivo:
# - Importa y registra modelos para que aparezcan en el panel de administración
#   incorporado de Django (`/admin/`). Esto permite CRUD básico desde el admin.
#
# Buenas prácticas y siguientes pasos posibles:
# - Personalizar listado y búsqueda:
#   Para controlar columnas mostradas, filtros, búsqueda y acciones, define
#   una clase que herede de `admin.ModelAdmin` y registra el modelo con esa
#   clase. Ejemplo (descomentar y adaptar si lo necesitas):
#
#   class TratamientoAdmin(admin.ModelAdmin):
#       list_display = ('id', 'nombre', 'precio')     # columnas en la lista
#       search_fields = ('nombre', 'descripcion')     # campos buscables
#       list_filter = ('precio',)                     # filtros laterales
#
#   admin.site.register(Tratamiento, TratamientoAdmin)
#
# - Seguridad: el admin de Django suele estar protegido por autenticación.
#   Mantén cuentas admin seguras y limita `is_superuser` a usuarios de confianza.
#
# - Integración con tu app: este proyecto usa vistas y plantillas propias para
#   la mayor parte del CRUD (interfaces públicas). Registrar los modelos aquí
#   es útil para tareas administrativas rápidas (debug, import/export, edición).
#
# - Si prefieres deshabilitar el acceso al admin en producción, remueve o
#   comenta estos `admin.site.register(...)` y/o restringe el acceso con middleware
#   o configuración de URLs.
#