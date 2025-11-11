"""
Configuración de Django para el proyecto `crud_project`.

Este archivo contiene ajustes generados por `startproject` y pequeñas
personalizaciones (por ejemplo, `app` en INSTALLED_APPS y un
context processor personalizado). Los comentarios aquí explican las
secciones relevantes de forma concisa.
"""

from pathlib import Path

# BASE_DIR: ruta absoluta a la carpeta base del proyecto.
# Se usa para construir rutas relativas (por ejemplo la base de datos).
BASE_DIR = Path(__file__).resolve().parent.parent


# ------------------------- Seguridad / despliegue -------------------------
# Importante: nunca dejes el SECRET_KEY en repositorio público en
# producción; aquí se mantiene para desarrollo local.
SECRET_KEY = 'django-insecure-=_7lp1q@d2jh*+r+v0l(z&0%dax)@twy)0drh&j08)w5w5bm8@'

# DEBUG True permite recargas automáticas y páginas de error detalladas.
# No debe estar activo en producción.
DEBUG = True

# Hosts permitidos por el servidor. En producción añade tu dominio.
ALLOWED_HOSTS = []


# ------------------------- Aplicaciones y middleware ---------------------
INSTALLED_APPS = [
    # Contrib de Django que proporcionan admin, auth, sesiones, archivos estáticos, etc.
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplicación local del proyecto donde están los modelos y vistas
    'app',
]

MIDDLEWARE = [
    # Pila de middleware estándar de Django. Cada elemento es una clase
    # que procesa requests/responses (seguridad, sesiones, CSRF, etc.).
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'crud_project.urls'  # Módulo que contiene las rutas principales


# ------------------------- Templates ------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Se pueden añadir rutas de templates globales aquí
        'APP_DIRS': True,  # Busca templates dentro de cada app/templates
        'OPTIONS': {
            'context_processors': [
                # Context processors predeterminados útiles en plantillas
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Processor personalizado definido en `app.context_processors`
                # que (según su nombre) expone roles de usuario en todas
                # las plantillas. Útil para mostrar/u ocultar UI según rol.
                'app.context_processors.user_roles',
            ],
        },
    },
]

WSGI_APPLICATION = 'crud_project.wsgi.application'  # Punto de entrada WSGI


# ------------------------- Base de datos --------------------------------
# Aquí se usa sqlite3 para desarrollo por simplicidad; en producción
# suele usarse PostgreSQL, MySQL, etc.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ------------------------- Validación de contraseñas --------------------
# Validadores que ayudan a endurecer contraseñas en producción.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# ------------------------- Internacionalización ------------------------
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ------------------------- Archivos estáticos ---------------------------
# URL base para servir archivos estáticos
STATIC_URL = '/static/'

# Redirecciones después de login/logout (rutas definidas en la app)
LOGIN_REDIRECT_URL = '/listar/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# Añadir carpeta de static personalizada (la app contiene app/statics)
from pathlib import Path as _Path
STATICFILES_DIRS = [
    BASE_DIR / 'app' / 'statics',
]


# Default primary key field type for modelos nuevos
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
