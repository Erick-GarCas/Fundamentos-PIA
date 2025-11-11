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