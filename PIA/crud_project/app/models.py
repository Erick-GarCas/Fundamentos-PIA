"""
Modelos del proyecto: Tratamiento, CitaDental, Usuario y Reservacion.

Cada modelo representa una entidad persistida en la base de datos.
"""

from django.db import models


def _upper_or_none(value):
	if isinstance(value, str):
		return value.strip().upper()
	return value


class Tratamiento(models.Model):
	nombre = models.CharField(max_length=150)
	descripcion = models.TextField(blank=True, null=True)
	precio = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.nombre

	def save(self, *args, **kwargs):
		self.nombre = _upper_or_none(self.nombre)
		if self.descripcion:
			self.descripcion = _upper_or_none(self.descripcion)
		super().save(*args, **kwargs)


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
		self.nombre_paciente = _upper_or_none(self.nombre_paciente)
		if self.estatus:
			self.estatus = _upper_or_none(self.estatus)
		super().save(*args, **kwargs)


class Usuario(models.Model):
	email = models.EmailField(unique=True, null=True, blank=True)
	password = models.CharField(max_length=128)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.email or f"usuario-{self.pk}"


class Reservacion(models.Model):
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
		fecha = self.fecha_reservacion.strftime('%Y-%m-%d %H:%M') if self.fecha_reservacion else 'SIN FECHA'
		return f"{self.nombre_cliente} - {fecha}"
