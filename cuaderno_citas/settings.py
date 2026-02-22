"""
=== SETTINGS DEL PROYECTO ===

Este archivo es donde se configura todo el proyecto.
Aquí va desde qué apps uso hasta dónde se guardan las imágenes.

CREDENCIALES PARA PROBAR:
- Admin: admin / admin123
- Usuario demo: demo / demo1234

"""

from pathlib import Path

# Esta es la ruta base del proyecto
# La uso para construir otras rutas (media, static, etc.)
BASE_DIR = Path(__file__).resolve().parent.parent

# La SECRET_KEY la usa Django para firmar cookies y tokens CSRF
# En producción debería estar en una variable de entorno, pero para clase vale así
SECRET_KEY = 'django-insecure-tu-clave-secreta-cambiala-en-produccion'

# DEBUG en True me muestra los errores completos en el navegador
# Muy útil mientras desarrollo, pero en producción hay que ponerlo en False
DEBUG = True

# Dominios permitidos para acceder
# Vacío permite localhost, que es lo que necesito ahora
ALLOWED_HOSTS = []


# Apps que uso en el proyecto
# Primero las de Django, luego las mías, luego las externas
INSTALLED_APPS = [
    # Apps que vienen con Django
    'django.contrib.admin',        # El panel /admin/
    'django.contrib.auth',         # Sistema de usuarios
    'django.contrib.contenttypes', # Para el sistema interno de Django
    'django.contrib.sessions',     # Para que funcione el login
    'django.contrib.messages',     # Para los mensajes tipo "Cita creada"
    'django.contrib.staticfiles',  # Para servir CSS y JS
    
    # Mis apps
    'core',     # Home y About
    'accounts', # Login, registro, logout
    'citas',    # La app principal
    
    # Apps externas que instalé con pip
    'crispy_forms',         # Para hacer los forms bonitos
    'crispy_bootstrap5',    # Templates de Bootstrap 5 para Crispy
]


# Los middleware son como filtros que pasan todas las peticiones
# Van en orden, es importante no cambiarlos de sitio
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Necesario para login
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección contra CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Para que funcione request.user
    'django.contrib.messages.middleware.MessageMiddleware',  # Para messages.success(), etc.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Le digo a Django dónde están las URLs principales
ROOT_URLCONF = 'cuaderno_citas.urls'


# Configuración de templates (los HTML)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        
        # DIRS es para templates globales (como base.html)
        # Los puse en /templates/ en la raíz del proyecto
        'DIRS': [BASE_DIR / 'templates'],
        
        # APP_DIRS=True hace que también busque en templates/ de cada app
        'APP_DIRS': True,
        
        'OPTIONS': {
            # Estos context_processors añaden variables a todos los templates
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Añade 'request'
                'django.contrib.auth.context_processors.auth',  # Añade 'user' y 'perms'
                'django.contrib.messages.context_processors.messages',  # Añade 'messages'
            ],
        },
    },
]

WSGI_APPLICATION = 'cuaderno_citas.wsgi.application'


# Base de datos
# Uso SQLite porque es lo más fácil para desarrollo
# El archivo se crea en la raíz: db.sqlite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Validación de contraseñas
# Django comprueba que las contraseñas no sean tontas
AUTH_PASSWORD_VALIDATORS = [
    {
        # Que no sea parecida al username
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        # Mínimo 8 caracteres
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        # Que no sea "123456" o "password"
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        # Que no sea solo números
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Idioma y zona horaria
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'Europe/Madrid'
USE_I18N = True
USE_TZ = True


# === ARCHIVOS STATIC (CSS, JS, imágenes del sitio) ===
# Estos son los archivos que forman parte del diseño
# NO son los que suben los usuarios (esos van en MEDIA)
STATIC_URL = '/static/'

# Aquí tengo mi carpeta static/ con CSS, JS e imágenes del diseño
STATICFILES_DIRS = [BASE_DIR / 'static']


# === ARCHIVOS MEDIA (imágenes subidas por usuarios) ===
# Aquí van las imágenes de citas que suben los usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# === CONFIGURACIÓN DE AUTENTICACIÓN ===

# Si intentas acceder a @login_required sin login, te manda aquí
LOGIN_URL = '/accounts/login/'

# Después de login exitoso, te manda aquí
LOGIN_REDIRECT_URL = '/citas/'

# Después de logout, te manda aquí
LOGOUT_REDIRECT_URL = '/'


# === CRISPY FORMS ===
# Para que los formularios se vean bonitos con Bootstrap
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


# Tipo de campo para las IDs automáticas
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'