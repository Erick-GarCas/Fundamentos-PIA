"""
Vistas principales de la aplicación.

Contiene vistas públicas (landing, cotizador, signup) y vistas CRUD
para los módulos: Citas, Tratamientos, Reservaciones y Usuarios.

Notas rápidas:
- Muchas vistas usan `messages` para feedback al usuario.
- Se usan decoradores de autorización (`login_required` y `group_required`)
  para restringir el acceso a ciertas acciones administrativas.
"""

from decimal import Decimal
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from .models import CitaDental, Reservacion, Tratamiento, Usuario

# ======= Resumen de dependencias y modelos =======
# - `CitaDental`, `Reservacion`, `Tratamiento`, `Usuario`: modelos usados en las vistas.
# - Utilizamos utilidades de Django: `messages`, `auth`, `decorators`, `transaction`.
# - Las vistas devuelven `render`, `redirect` o `JsonResponse` según corresponda.


def _is_past_day(dt_obj):
	"""Devuelve True si la fecha dada corresponde a un día anterior al actual."""

# Helper - Validación de fecha
# - Entrada: `dt_obj` (datetime/None).
# - Salida: True si la fecha pertenece a un día anterior al día actual.
# - Uso frecuente para evitar agendar o reprogramar eventos en el pasado.
	if dt_obj is None:
		return True
	if timezone.is_aware(dt_obj):
		dt_obj = timezone.localtime(dt_obj)
	target_date = dt_obj.date()
	today = timezone.localdate()
	return target_date < today


def index(request):
	"""Renderiza la landing page (index.html) ubicada en `app/templates/index.html`."""
	return render(request, 'index.html')

# Public view - Página principal
# - Método: GET
# - Template: `index.html`
# - No requiere autenticación.


def solicitar_cita(request):
	"""Recibe POST desde el formulario tradicional y crea una CitaDental simple.
	   Reglas:
	   - nombre (required), telefono (required), tratamientos[] (1-2), fecha-cita (required)
	   - no permitir dos citas en la misma hora (año/mes/día/hora)
	"""
	if request.method != 'POST':
		return redirect('home')

	nombre = request.POST.get('nombre', '').strip()
	telefono = request.POST.get('telefono', '').strip()
	correo = request.POST.get('correo', '').strip()
	tratamientos_ids = request.POST.getlist('tratamiento[]') or request.POST.getlist('tratamiento')
	fecha_val = request.POST.get('fecha-cita') or request.POST.get('fecha_cita')

	# Validaciones básicas
	if not nombre or not telefono or not fecha_val or not tratamientos_ids:
		messages.error(request, 'Faltan datos requeridos. Por favor complete nombre, teléfono, fecha y al menos un tratamiento.')
		return redirect('home')

# Vista pública para solicitar cita
# - Recibe datos por POST provenientes del formulario público.
# - Valida campos mínimos, formato de correo y fecha futura.
# - Evita duplicados por hora: si ya hay una cita a la misma hora devuelve error.
# - Crea un registro `CitaDental` y asocia hasta 2 `Tratamiento`.

	if len(tratamientos_ids) > 2:
		messages.error(request, 'Sólo se permiten hasta 2 tratamientos por solicitud.')
		return redirect('home')

	if correo:
		try:
			validate_email(correo)
		except ValidationError:
			messages.error(request, 'El correo proporcionado no es válido.')
			return redirect('home')

	# Parsear fecha
	fecha = parse_datetime(fecha_val)
	if fecha is None:
		# intentar parse simple reemplazando espacio T si es necesario
		try:
			from datetime import datetime
			fecha = datetime.fromisoformat(fecha_val)
		except Exception:
			fecha = None

	if fecha is None:
		messages.error(request, 'Formato de fecha inválido.')
		return redirect('home')

	if _is_past_day(fecha):
		messages.error(request, 'La fecha debe ser igual o posterior a hoy.')
		return redirect('home')

	# Comprobar conflicto (mismo año/mes/día/hora)
	conflict = CitaDental.objects.filter(
		fecha_cita__year=fecha.year,
		fecha_cita__month=fecha.month,
		fecha_cita__day=fecha.day,
		fecha_cita__hour=fecha.hour,
	).exists()

	if conflict:
		messages.error(request, 'Ya existe una cita en esa hora. Elija otro horario.')
		return redirect('home')

	# Crear cita
	cita = CitaDental.objects.create(
		nombre_paciente=nombre,
		fecha_cita=fecha,
		telefono=telefono,
		correo=correo or None,
	)

	# Asociar tratamientos (ignorar ids inválidos)
	tratamientos_objs = Tratamiento.objects.filter(id__in=tratamientos_ids)[:2]
	if tratamientos_objs:
		cita.tratamientos.set(tratamientos_objs)

	messages.success(request, 'La cita fue solicitada correctamente. Nos pondremos en contacto para confirmar.')
	return redirect('home')


def tratamientos_json(request):
	"""Devuelve la lista de tratamientos en formato JSON para que el frontend los consuma.
	   Cada objeto incluye id, nombre, descripcion, precio (float) y precioTexto.
	"""
	qs = Tratamiento.objects.all()
	data = []
	for t in qs:
		data.append({
			'id': t.id,
			'nombre': t.nombre,
			'descripcion': t.descripcion or '',
			'precio': float(t.precio),
			'precioTexto': f"${t.precio} MXN",
		})
	return JsonResponse(data, safe=False)

# API simple para listar tratamientos
# - Uso desde JavaScript: consume un arreglo JSON con detalles (id, nombre, descripcion, precio).
# - No requiere autenticación.


def signup(request):
	"""Registro simple de usuario. Crea un User y lo autentica en la sesión.
	   Campos esperados (POST): username, email (opcional), password1, password2
	"""
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		p1 = request.POST.get('password1', '')
		p2 = request.POST.get('password2', '')

		if not username or not p1 or not p2:
			messages.error(request, 'Por favor complete usuario y contraseña.')
			return redirect('signup')

		if p1 != p2:
			messages.error(request, 'Las contraseñas no coinciden.')
			return redirect('signup')

		# Validaciones
		if User.objects.filter(username=username).exists():
			messages.error(request, 'El nombre de usuario ya está en uso.')
			return redirect('signup')

		# Si se proporcionó email, verificar que no exista en nuestro modelo Usuario
		if email:
			if Usuario.objects.filter(email=email).exists() or User.objects.filter(email=email).exists():
				messages.error(request, 'El correo ya está en uso. Use otro correo o inicie sesión.')
				return redirect('signup')

		# Crear ambos registros dentro de una transacción: User y Usuario espejo
		try:
			with transaction.atomic():
				user = User.objects.create_user(username=username, email=email, password=p1)
				user.save()
				# Crear registro espejo en el modelo Usuario (almacenar email y contraseña hasheada)
				email_val = email if email else None
				Usuario.objects.create(email=email_val, password=make_password(p1))
		except Exception:
			# Rollback automático por atomic(); informar al usuario
			messages.error(request, 'Error al crear la cuenta. Por favor intente nuevamente.')
			return redirect('signup')

		# Redirigir al login para que el usuario compruebe sus credenciales
		messages.success(request, 'Cuenta creada correctamente. Por favor inicia sesión.')
		return redirect('login')

	# GET -> render formulario de registro
	return render(request, 'signup.html')

# Registro de usuario
# - POST: valida datos, evita duplicados y crea dos registros: `User` y `Usuario` (espejo).
# - Se usa `transaction.atomic()` para que la creación sea atómica.
# - Mensajes al usuario mediante `messages` y redirección a `login`.


def login_view(request):
	"""Vista de login personalizada para usar la plantilla `login.html`."""
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		next_url = request.POST.get('next') or 'listar'
		user = authenticate(request, username=username, password=password)
		if user:
			auth_login(request, user)
			return redirect(next_url)
		messages.error(request, 'Credenciales inválidas. Intente de nuevo.')
	next_url = request.GET.get('next', '')
	return render(request, 'login.html', {'next': next_url})

# Login personalizado
# - POST: intenta autenticar y redirige a `next` o a `listar`.
# - GET: muestra el formulario de login y puede recibir `next` en querystring.
# - Usa `messages` para feedback en credenciales inválidas.


@login_required
def listar(request):
	"""Renderiza el template de listado (`listar.html`)."""
	ensure_default_groups()
	try:
		count_citas = CitaDental.objects.count()
	except Exception:
		count_citas = 0
	try:
		count_tratamientos = Tratamiento.objects.count()
	except Exception:
		count_tratamientos = 0

	recent_citas = CitaDental.objects.all().order_by('-fecha_cita')[:5]
	is_admin = False
	is_employee = False
	if request.user and request.user.is_authenticated:
		is_admin = request.user.is_superuser or request.user.groups.filter(name='Administrador').exists()
		is_employee = request.user.groups.filter(name='Empleado').exists()
	return render(request, 'listar.html', {
		'count_citas': count_citas,
		'count_tratamientos': count_tratamientos,
		'recent_citas': recent_citas,
		'is_admin': is_admin,
		'is_employee': is_employee,
	})

# Dashboard administrativo / resumen
# - Requiere login.
# - Muestra contadores y últimas citas para dar una vista rápida al usuario autenticado.
# - Calcula flags `is_admin` y `is_employee` para condicionar la UI.


def group_required(*group_names):
	"""Decorator to require user to be member of at least one group."""
	def decorator(view_func):
		@wraps(view_func)
		def _wrapped(request, *args, **kwargs):
			if not request.user.is_authenticated:
				return redirect('login')
			if request.user.is_superuser:
				return view_func(request, *args, **kwargs)
			if request.user.groups.filter(name__in=group_names).exists():
				return view_func(request, *args, **kwargs)
			return HttpResponseForbidden('No tienes permisos para acceder a esta página.')
		return _wrapped
	return decorator

# Decorador `group_required`
# - Usa grupos de Django para controlar acceso (ej: 'Administrador', 'Empleado').
# - Si el usuario es `superuser` se permite el acceso automáticamente.
# - Si no está autenticado redirige a `login`, si no pertenece a los grupos retorna 403.


def ensure_default_groups():
	"""Garantiza que existan los grupos base y permisos de módulos."""
	try:
		for name in ('Administrador', 'Empleado', 'Permiso Citas', 'Permiso Tratamientos'):
			Group.objects.get_or_create(name=name)
	except Exception:
		pass

# Inicialización de grupos por defecto
# - Se puede llamar antes de mostrar listas de usuarios o al iniciar ciertos workflows.
# - Silenciosamente ignora errores para evitar romper vistas por problemas en el ORM.


def assign_user_groups(user_obj, role_admin=False, role_employee=False, perm_citas=False, perm_tratamientos=False):
	"""Asigna grupos al usuario según los flags enviados."""
	ensure_default_groups()
	group_map = {
		'admin': Group.objects.get(name='Administrador'),
		'employee': Group.objects.get(name='Empleado'),
		'citas': Group.objects.get(name='Permiso Citas'),
		'tratamientos': Group.objects.get(name='Permiso Tratamientos'),
	}
	user_obj.groups.clear()
	if role_admin:
		user_obj.groups.add(group_map['admin'])
	if role_employee:
		user_obj.groups.add(group_map['employee'])
	if perm_citas:
		user_obj.groups.add(group_map['citas'])
	if perm_tratamientos:
		user_obj.groups.add(group_map['tratamientos'])

# Función utilitaria para asignar roles y permisos a un `User`:
# - `role_admin`, `role_employee`: roles de alto nivel.
# - `perm_citas`, `perm_tratamientos`: permisos por módulo.
# - Primero limpia los grupos existentes y luego asigna los seleccionados.


@login_required
@group_required('Administrador', 'Empleado', 'Permiso Citas')
def citas_listar(request):
	qs = CitaDental.objects.all().prefetch_related('tratamientos').order_by('-fecha_cita')
	return render(request, 'citas_listar.html', {'citas': qs})

# CRUD Citas - Listar
# - Requiere pertenecer a al menos uno de los grupos listados en el decorador.
# - `prefetch_related` optimiza la carga de tratamientos relacionados.


@login_required
@group_required('Administrador')
def citas_crear(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre_paciente', '').strip()
		telefono = request.POST.get('telefono', '').strip()
		correo = request.POST.get('correo', '').strip()
		fecha_val = request.POST.get('fecha_cita')
		if not nombre or not telefono or not fecha_val:
			messages.error(request, 'Faltan datos requeridos.')
			return redirect('citas_crear')
		if correo:
			try:
				validate_email(correo)
			except ValidationError:
				messages.error(request, 'El correo proporcionado no es válido.')
				return redirect('citas_crear')
		fecha = parse_datetime(fecha_val)
		if fecha is None:
			messages.error(request, 'Formato de fecha inválido.')
			return redirect('citas_crear')
		if _is_past_day(fecha):
			messages.error(request, 'La fecha debe ser igual o posterior a hoy.')
			return redirect('citas_crear')
		CitaDental.objects.create(
			nombre_paciente=nombre,
			telefono=telefono,
			correo=correo or None,
			fecha_cita=fecha
		)
		messages.success(request, 'Cita creada correctamente.')
		return redirect('citas_listar')
	return render(request, 'citas_crear.html')

# CRUD Citas - Crear
# - Solo administradores pueden crear desde el panel.
# - Valida campos obligatorios y que la fecha no sea pasada.
# - Muestra mensajes de éxito/error y redirige a la lista.


@login_required
@group_required('Administrador', 'Empleado')
def citas_editar(request, id):
	cita = get_object_or_404(CitaDental, pk=id)
	if request.method == 'POST':
		fecha_val = request.POST.get('fecha_cita')
		if not fecha_val:
			messages.error(request, 'Debes seleccionar una fecha y hora')
			return redirect('citas_editar', id=id)
		fecha = parse_datetime(fecha_val)
		if fecha is None:
			messages.error(request, 'Fecha inválida.')
			return redirect('citas_editar', id=id)
		if _is_past_day(fecha):
			messages.error(request, 'La fecha debe ser igual o posterior a hoy.')
			return redirect('citas_editar', id=id)
		cita.fecha_cita = fecha
		cita.save(update_fields=['fecha_cita'])
		messages.success(request, 'Cita reprogramada exitosamente')
		return redirect('citas_listar')
	return render(request, 'citas_editar.html', {'cita': cita})

# CRUD Citas - Editar
# - Admins y empleados pueden reprogramar la fecha de una cita.
# - Evita poner una fecha en el pasado y guarda únicamente el campo `fecha_cita`.


@login_required
@group_required('Administrador', 'Empleado')
def citas_eliminar(request, id):
	if request.method != 'POST':
		return redirect('citas_listar')
	cita = get_object_or_404(CitaDental, pk=id)
	cita.delete()
	messages.success(request, 'Cita eliminada')
	return redirect('citas_listar')

# CRUD Citas - Eliminar
# - Solo POST para seguridad (evita borrar por GET accidentalmente).
# - Muestra feedback mediante `messages`.


@login_required
@group_required('Administrador', 'Empleado', 'Permiso Citas')
def citas_marcar_listo(request, id):
	cita = get_object_or_404(CitaDental, pk=id)
	cita.estatus = CitaDental.ESTATUS_ATENDIDA
	cita.save()
	messages.success(request, 'Cita marcada como atendida')
	return redirect('citas_listar')

# Acción: marcar cita como atendida
# - Cambia el estatus interno y redirige a la lista.
# - Útil para el flujo de trabajo del personal.


@login_required
@group_required('Administrador', 'Permiso Tratamientos')
def tratamientos_listar(request):
	tratamientos = Tratamiento.objects.all().order_by('nombre')
	return render(request, 'tratamientos_list.html', {'tratamientos': tratamientos})

# CRUD Tratamientos - Listar
# - Requiere permisos específicos de tratamiento o ser Administrador.
# - Usado por el personal para ver y seleccionar tratamientos.


@login_required
@group_required('Administrador', 'Permiso Tratamientos')
def tratamientos_crear(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		descripcion = request.POST.get('descripcion', '').strip()
		precio_val = request.POST.get('precio', '').strip()

		if not nombre or not precio_val:
			messages.error(request, 'Nombre y precio son obligatorios')
			return redirect('tratamientos_crear')
		try:
			precio = Decimal(precio_val)
		except Exception:
			messages.error(request, 'Ingrese un precio válido')
			return redirect('tratamientos_crear')

		Tratamiento.objects.create(nombre=nombre, descripcion=descripcion or '', precio=precio)
		messages.success(request, 'Tratamiento creado correctamente')
		return redirect('tratamientos_listar')
	return render(request, 'tratamientos_form.html')

# CRUD Tratamientos - Crear
# - Valida que nombre y precio existan y que el precio sea convertible a Decimal.
# - Guarda el objeto `Tratamiento` y redirige a la lista con mensaje de éxito.


@login_required
@group_required('Administrador', 'Permiso Tratamientos')
def tratamientos_editar(request, id):
	tratamiento = get_object_or_404(Tratamiento, pk=id)
	if request.method == 'POST':
		nombre = request.POST.get('nombre', '').strip()
		descripcion = request.POST.get('descripcion', '').strip()
		precio_val = request.POST.get('precio', '').strip()

		if not nombre or not precio_val:
			messages.error(request, 'Nombre y precio son obligatorios')
			return redirect('tratamientos_editar', id=id)
		try:
			precio = Decimal(precio_val)
		except Exception:
			messages.error(request, 'Ingrese un precio válido')
			return redirect('tratamientos_editar', id=id)

		tratamiento.nombre = nombre
		tratamiento.descripcion = descripcion
		tratamiento.precio = precio
		tratamiento.save()
		messages.success(request, 'Tratamiento actualizado')
		return redirect('tratamientos_listar')
	return render(request, 'tratamientos_form.html', {'tratamiento': tratamiento})

# CRUD Tratamientos - Editar
# - Recupera el objeto, valida los datos y actualiza los campos permitidos.
# - Mantiene UI unificada reutilizando `tratamientos_form.html`.


@login_required
@group_required('Administrador', 'Permiso Tratamientos')
def tratamientos_eliminar(request, id):
	if request.method != 'POST':
		return redirect('tratamientos_listar')
	tratamiento = get_object_or_404(Tratamiento, pk=id)
	tratamiento.delete()
	messages.success(request, 'Tratamiento eliminado')
	return redirect('tratamientos_listar')

# CRUD Tratamientos - Eliminar
# - Solo por POST; elimina el registro y muestra mensaje de confirmación.


@login_required
@group_required('Administrador', 'Empleado')
def reservaciones_listar(request):
	qs = Reservacion.objects.all().order_by('-fecha_reservacion')
	return render(request, 'reservaciones_listar.html', {'reservaciones': qs})

# CRUD Reservaciones - Listar
# - Muestra las reservaciones ordenadas por fecha.
# - Acceso restringido según roles.


@login_required
@group_required('Administrador')
def reservaciones_crear(request):
	if request.method == 'POST':
		nombre = request.POST.get('nombre_cliente', '').strip()
		fecha_val = request.POST.get('fecha_reservacion')
		telefono = request.POST.get('telefono', '').strip()
		asistentes = request.POST.get('asistentes') or 0
		if not nombre or not fecha_val:
			messages.error(request, 'Faltan datos requeridos')
			return redirect('reservaciones_listar')
		fecha = parse_datetime(fecha_val)
		if fecha is None:
			messages.error(request, 'Formato de fecha inválido')
			return redirect('reservaciones_listar')
		Reservacion.objects.create(
			nombre_cliente=nombre,
			fecha_reservacion=fecha,
			telefono=telefono,
			asistentes=int(asistentes)
		)
		messages.success(request, 'Reservación creada correctamente')
		return redirect('reservaciones_listar')
	return render(request, 'reservaciones_form.html')

# CRUD Reservaciones - Crear
# - Solo administradores: crea una reservación con nombre, fecha, teléfono y asistentes.
# - Convierte `asistentes` a entero antes de guardar.


@login_required
@group_required('Administrador')
def reservaciones_editar(request, id):
	r = get_object_or_404(Reservacion, pk=id)
	if request.method == 'POST':
		r.nombre_cliente = request.POST.get('nombre_cliente', r.nombre_cliente)
		fecha_val = request.POST.get('fecha_reservacion')
		fecha = parse_datetime(fecha_val) if fecha_val else r.fecha_reservacion
		if fecha:
			r.fecha_reservacion = fecha
		r.telefono = request.POST.get('telefono', r.telefono)
		r.asistentes = int(request.POST.get('asistentes') or r.asistentes)
		r.save()
		messages.success(request, 'Reservación actualizada')
		return redirect('reservaciones_listar')
	return render(request, 'reservaciones_form.html', {'reservacion': r})

# CRUD Reservaciones - Editar
# - Actualiza campos opcionales si se envían en POST, preservando valores por defecto.
# - Redirige a la lista y muestra mensaje de éxito.


@login_required
@group_required('Administrador')
def reservaciones_eliminar(request, id):
	if request.method != 'POST':
		return redirect('reservaciones_listar')
	r = get_object_or_404(Reservacion, pk=id)
	r.delete()
	messages.success(request, 'Reservación eliminada')
	return redirect('reservaciones_listar')

# CRUD Reservaciones - Eliminar
# - Solo POST; elimina el registro identificado por `id`.


@login_required
@group_required('Administrador', 'Empleado')
def reservaciones_marcar_listo(request, id):
	r = get_object_or_404(Reservacion, pk=id)
	r.estatus = Reservacion.ESTATUS_LISTA
	r.save()
	messages.success(request, 'Reservación marcada como lista')
	return redirect('reservaciones_listar')

# Acción: marcar reservación como lista
# - Útil para indicar que la reservación ya fue atendida/preparada.


@login_required
@group_required('Administrador')
def usuarios_listar(request):
	ensure_default_groups()
	qs = User.objects.all().order_by('username')
	return render(request, 'users_list.html', {'usuarios': qs})

# Gestión de Usuarios - Listar
# - Inicializa grupos (si faltan) y lista todos los `User`.
# - Solo accesible por Administradores.


@login_required
@group_required('Administrador')
def usuarios_crear(request):
	ensure_default_groups()
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		role_admin = True if request.POST.get('role_admin') == 'on' else False
		role_employee = True if request.POST.get('role_employee') == 'on' else False
		perm_citas = True if request.POST.get('perm_citas') == 'on' else False
		perm_tratamientos = True if request.POST.get('perm_tratamientos') == 'on' else False
		is_superuser = True if request.POST.get('is_superuser') == 'on' else False

		if not username or not password:
			messages.error(request, 'Usuario y contraseña son requeridos')
			return redirect('usuarios_listar')

		if User.objects.filter(username=username).exists():
			messages.error(request, 'El nombre de usuario ya existe')
			return redirect('usuarios_listar')

		u = User.objects.create_user(username=username, email=email, password=password)
		u.is_superuser = is_superuser
		u.is_staff = is_superuser or role_admin or role_employee or perm_citas or perm_tratamientos
		u.save()
		assign_user_groups(u, role_admin, role_employee, perm_citas, perm_tratamientos)

		messages.success(request, 'Usuario creado correctamente')
		return redirect('usuarios_listar')

	return render(request, 'users_create.html', {
		'role_flags': {'admin': False, 'employee': False},
		'perm_flags': {'citas': False, 'tratamientos': False},
		'superuser_flag': False,
	})

# Gestión de Usuarios - Crear
# - Permite crear un usuario administrativo o con permisos específicos.
# - Asigna flags y grupos via `assign_user_groups`.
# - Marca `is_staff` si el usuario tiene cualquier rol o permiso relevante.


@login_required
@group_required('Administrador')
def usuarios_editar(request, id):
	ensure_default_groups()
	user_obj = get_object_or_404(User, pk=id)
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		email = request.POST.get('email', '').strip()
		password = request.POST.get('password', '')
		role_admin = True if request.POST.get('role_admin') == 'on' else False
		role_employee = True if request.POST.get('role_employee') == 'on' else False
		perm_citas = True if request.POST.get('perm_citas') == 'on' else False
		perm_tratamientos = True if request.POST.get('perm_tratamientos') == 'on' else False
		is_superuser = True if request.POST.get('is_superuser') == 'on' else False

		if username:
			user_obj.username = username
		user_obj.email = email
		if password:
			user_obj.set_password(password)
		user_obj.is_staff = is_superuser or role_admin or role_employee or perm_citas or perm_tratamientos
		user_obj.is_superuser = is_superuser
		user_obj.save()
		assign_user_groups(user_obj, role_admin, role_employee, perm_citas, perm_tratamientos)

		messages.success(request, 'Usuario actualizado')
		return redirect('usuarios_listar')

	role_flags = {
		'admin': user_obj.groups.filter(name='Administrador').exists(),
		'employee': user_obj.groups.filter(name='Empleado').exists(),
	}
	perm_flags = {
		'citas': user_obj.groups.filter(name='Permiso Citas').exists(),
		'tratamientos': user_obj.groups.filter(name='Permiso Tratamientos').exists(),
	}
	return render(request, 'users_edit.html', {
		'user_obj': user_obj,
		'role_flags': role_flags,
		'perm_flags': perm_flags,
		'superuser_flag': user_obj.is_superuser,
	})

# Gestión de Usuarios - Editar
# - Actualiza username, email, password y flags de rol/permiso.
# - No permite cambiar la propia eliminación desde esta vista (ver `usuarios_eliminar`).


@login_required
@group_required('Administrador')
def usuarios_eliminar(request, id):
	if request.method != 'POST':
		return redirect('usuarios_listar')
	user_obj = get_object_or_404(User, pk=id)
	if request.user.pk == user_obj.pk:
		messages.error(request, 'No puedes eliminarte a ti mismo')
		return redirect('usuarios_listar')
	user_obj.delete()
	messages.success(request, 'Usuario eliminado.')
	return redirect('usuarios_listar')

# Gestión de Usuarios - Eliminar
# - Previene que un usuario se elimine a sí mismo.
# - Solo POST para prevenir borrados accidentales.


def crear(request):
	"""Vista placeholder para crear un contacto."""
	if request.method == 'POST':
		messages.success(request, 'Contacto creado correctamente.')
		return redirect('listar')
	return render(request, 'crear.html')

# Vistas placeholder: `crear`, `editar`, `eliminar`
# - Plantillas de ejemplo usados por la UI. Conservadas para compatibilidad.


def editar(request, id):
	"""Vista placeholder para editar un contacto."""
	if request.method == 'POST':
		messages.success(request, 'Contacto actualizado correctamente.')
		return redirect('listar')
	return render(request, 'editar.html', {'id': id})


def eliminar(request, id):
	"""Elimina un contacto (placeholder)."""
	if request.method != 'POST':
		return redirect('listar')
	messages.success(request, 'Contacto eliminado.')
	return redirect('listar')
