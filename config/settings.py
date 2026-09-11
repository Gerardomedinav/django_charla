"""
Django settings for el_restaurante_de_django project.
Desarrollado para el laboratorio interactivo FORMO DEV.
"""

from pathlib import Path
import os

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga de variables de entorno desde .env si existe
env_path = BASE_DIR / '.env'
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ.setdefault(key.strip(), val.strip())

# Seguridad
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-formo-dev-super-secreta-restaurante-2025-clave-segura'
)

DEBUG = os.environ.get('DEBUG', 'True').lower() in ('true', '1', 'yes')

ALLOWED_HOSTS = [h.strip() for h in os.environ.get('ALLOWED_HOSTS', '*').split(',') if h.strip()]

# Configuración Google Gemini API - El Sensei Formoseño
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
GEMINI_MODEL = os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash')

# Aplicaciones instaladas (Separación modular por capas)
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# Daphne y Channels opcionales (habilitados en Docker/ASGI, ignorados limpiamente en PythonAnywhere/WSGI)
try:
    import daphne
    DJANGO_APPS.insert(0, 'daphne')
except ImportError:
    pass

THIRD_PARTY_APPS = []
try:
    import channels
    THIRD_PARTY_APPS.append('channels')
except ImportError:
    pass

LOCAL_APPS = [
    'core.apps.CoreConfig',
    'restaurante.apps.RestauranteConfig',
    'laboratorio.apps.LaboratorioConfig',
    'notificaciones.apps.NotificacionesConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'core' / 'templates',
            BASE_DIR / 'restaurante' / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application'

# Django Channels Layer (In-Memory para desarrollo y laboratorio)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}

# Configuración de Base de Datos Inteligente (PostgreSQL en Docker / SQLite en Host local)
import socket

DB_HOST = os.environ.get('DB_HOST')

def can_resolve_host(host):
    if not host:
        return False
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False

if DB_HOST and can_resolve_host(DB_HOST):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('POSTGRES_DB', 'restaurante_db'),
            'USER': os.environ.get('POSTGRES_USER', 'formodev'),
            'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'formodev_password_segura'),
            'HOST': DB_HOST,
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Validación de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Backends de autenticación (permite login por username o por email)
AUTHENTICATION_BACKENDS = [
    'restaurante.backends.EmailOrUsernameModelBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Internacionalización
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    d for d in [
        BASE_DIR / 'restaurante' / 'static',
        BASE_DIR / 'asset',
        BASE_DIR / 'assets',
    ] if d.exists()
]
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://*.pythonanywhere.com',
]
