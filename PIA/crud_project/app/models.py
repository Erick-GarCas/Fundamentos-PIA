"""
Modelos del proyecto: Tratamiento, CitaDental, Usuario y Reservacion.

Cada modelo representa una entidad persistida en la base de datos.
Se mantienen sencillos para fines de la práctica: campos claros y
representación en __str__ para visualización en el admin y UI.
"""

from django.db import models

# Modelo de tratamiento (TRATAMIENTO)
# Campos: nombre, descripcion, precio
class Tratamiento(models.Model):
	nombre = models.CharField(max_length=150)
	descripcion = models.TextField(blank=True, null=True)
	precio = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nombre


# Modelo de cita dental (CITA_DENTAL)
# Campos: nombre_paciente, procedimiento (relación con Tratamiento), fecha_cita,
# telefono, correo, estatus
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
	# Permitir asociar varios tratamientos a una cita (hasta 2 en la UI)
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
		# Muestra nombre del paciente y fecha breve para identificación
		fecha = self.fecha_cita.strftime('%Y-%m-%d %H:%M') if self.fecha_cita else 'Sin fecha'
		return f"{self.nombre_paciente} — {fecha}"


class Usuario(models.Model):
	"""Modelo simple para control de usuarios con correo y contraseña hasheada.

	Se crea al registrarse desde el formulario de signup. Este modelo guarda el
	email (opcional) y la contraseña en formato hasheado (usando las utilidades
	de django.contrib.auth.hashers desde la vista al crear el registro).
	"""
	email = models.EmailField(unique=True, null=True, blank=True)
	# Guardamos la contraseña hasheada (max_length acorde a los hashers de Django)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email or f"usuario-{self.pk}"


class Reservacion(models.Model):
	"""Reservaciones para salón de fiestas (salón de eventos).

	Campos sencillos para demostración académica.
	"""
	ESTATUS_PENDIENTE = 'PENDIENTE'
	ESTATUS_CONFIRMADA = 'CONFIRMADA'
	ESTATUS_CANCELADA = 'CANCELADA'
	ESTATUS_LISTA = 'LISTA'

	ESTATUS_CHOICES = [
		(ESTATUS_PENDIENTE, 'Pendiente'),
		(ESTATUS_CONFIRMADA, 'Confirmada'),
		(ESTATUS_CANCELADA, 'Cancelada'),
		(ESTATUS_LISTA, 'Lista'),
	]

	nombre_cliente = models.CharField(max_length=200)
	fecha_reservacion = models.DateTimeField()
	telefono = models.CharField(max_length=30, blank=True, null=True)
	correo = models.EmailField(blank=True, null=True)
	asistentes = models.PositiveIntegerField(default=0)
	estatus = models.CharField(max_length=20, choices=ESTATUS_CHOICES, default=ESTATUS_PENDIENTE)

	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		fecha = self.fecha_reservacion.strftime('%Y-%m-%d %H:%M') if self.fecha_reservacion else 'Sin fecha'
		return f"{self.nombre_cliente} — {fecha}"