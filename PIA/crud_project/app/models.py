
# Modelos del proyecto: Tratamiento, CitaDental, Usuario.
#
# Este módulo contiene las entidades persistidas en la base de datos.
# Los comentarios en cada clase explican por qué se eligieron ciertos tipos
# de campo y qué consideraciones tener al operar con ellos.
#
# Notas generales:
# - Si el proyecto crece y requiere autenticación robusta, considere usar
#   `django.contrib.auth.models.User` en lugar de un modelo `Usuario` propio.
#   El campo `password` aquí no aplica hashing automáticamente; asegúrese de
#   que las contraseñas se guarden usando funciones de hash (p. ej. `make_password`).
# - Campos como `DateTimeField` representan un momento específico; para
#   búsquedas por hora puede ser útil normalizar o indexar según requisitos.

from django.db import models



def _upper_or_none(value):
	# Helper sencillo: si el valor es string, limpiar espacios y convertir
	# a mayúsculas. Usado para normalizar texto antes de persistirlo.
	if isinstance(value, str):
		return value.strip().upper()
	return value



# Representa un tratamiento/servicio ofrecido.
#
# Campos clave:
# - `nombre`: CharField con longitud limitada (150) para nombre legible.
# - `descripcion`: TextField opcional para detalles largos.
# - `precio`: DecimalField para evitar errores de precisión con floats.
#
# Notas:
# - `precio` usa `max_digits=10` y `decimal_places=2` para cubrir precios
#   con dos decimales (moneda). Ajustar según rango de precios esperado.
# - `save()` sobrescrito normaliza texto (mayúsculas) para consistencia.

class Tratamiento(models.Model):
	nombre = models.CharField(max_length=150)
	descripcion = models.TextField(blank=True, null=True)
	precio = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		# Normalizar texto antes de persistir: útil para búsquedas y presentación.
		self.nombre = _upper_or_none(self.nombre)
		if self.descripcion:
			self.descripcion = _upper_or_none(self.descripcion)
		super().save(*args, **kwargs)



# Modelo que representa una cita dental asociada a uno o más tratamientos.
#
# Diseño y decisiones:
# - Se usan constantes para los `estatus` y una lista `ESTATUS_CHOICES` para
#   facilitar la selección en formularios y admin.
# - `tratamientos` es ManyToMany porque una cita puede incluir varios servicios.
# - `fecha_cita` es DateTimeField para permitir fecha y hora precisas.
# - `telefono` y `correo` son opcionales (blank/null) para aceptar registros
#   que no siempre proporcionen contacto.
#
# Consideraciones:
# - No existe una restricción de unicidad en `fecha_cita` -> se pueden crear
#   colisiones de horario; si el negocio requiere evitar reservas simultáneas,
#   agregue una restricción o gestione a nivel de vista/transaction.


class CitaDental(models.Model):
	ESTATUS_PENDIENTE = 'PENDIENTE'
	ESTATUS_CONFIRMADA = 'CONFIRMADA'
	ESTATUS_CANCELADA = 'CANCELADA'
	ESTATUS_ATENDIDA = 'ATENDIDA'

	ESTATUS_CHOICES = [
		(ESTATUS_PENDIENTE, 'Pendiente'),
		(ESTATUS_CONFIRMADA, 'Confirmada'),
		(ESTATUS_CANCELADA, 'Cancelada'),
		(ESTATUS_ATENDIDA, 'Atendida'),
	]

	nombre_paciente = models.CharField(max_length=200)
	tratamientos = models.ManyToManyField(
		Tratamiento,
		blank=True,
		related_name='citas',
		help_text='Tratamientos asociados a la cita'
	)
	fecha_cita = models.DateTimeField()
	telefono = models.CharField(max_length=30, blank=True, null=True)
	correo = models.EmailField(blank=True, null=True)
	estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ESTATUS_PENDIENTE)

	def __str__(self):
		fecha = self.fecha_cita.strftime('%Y-%m-%d %H:%M') if self.fecha_cita else 'SIN FECHA'
		return f"{self.nombre_paciente} - {fecha}"

	def save(self, *args, **kwargs):
		# Normalizar nombre del paciente y estado antes de guardar.
		self.nombre_paciente = _upper_or_none(self.nombre_paciente)
		if self.estatus:
			self.estatus = _upper_or_none(self.estatus)
		super().save(*args, **kwargs)



# Modelo mínimo para representar credenciales básicas.
#
# Advertencia:
# - Este modelo almacena `password` en un CharField pero no gestiona hashing.
#   Para seguridad, las contraseñas deben ser hashed (p. ej. `make_password`)
#   o usar el sistema de usuarios de Django (`AbstractUser`/`User`).
#
# - El campo `email` es `unique=True` para evitar duplicados en la tabla.
#   Sin embargo, `null=True, blank=True` permite registros sin email —
#   considere exigir email si es un identificador principal.


class Usuario(models.Model):
	email = models.EmailField(unique=True, null=True, blank=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email or f"usuario-{self.pk}"