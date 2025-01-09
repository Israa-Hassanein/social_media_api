from pathlib import Path
import os
import environ
from decouple import config
import dj_database_url
from decouple import Config, Csv
from decouple import config

LOGIN_REDIRECT_URL = '/'  # Redirect to home after successful login


# Initialize the environment variable reader
env = environ.Env()
# Read the environment variables from the .env file
env.read_env()

ENVIRONMENT = env('ENVIRONMENT', default='production')
# Load the SECRET_KEY from the environment
SECRET_KEY = env('SECRET_KEY')

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgres://localhost'),
        conn_max_age=600,
        ssl_require=True
    )
}


BASE_DIR = Path(__file__).resolve().parent.parent
ALLOWED_HOSTS = [
    'esraahassanein.pythonanywhere.com',
    'localhost',
    'socialmediaapi-production-f067.up.railway.app',
    '127.0.0.1'
]

CSRF_TRUSTED_ORIGINS = ['https://socialmediaapi-production-f067.up.railway.app']

INTERNAL_IPS = ('127.0.0.1', 'localhost:8000')
PORT = int(os.environ.get("PORT", 8080)) 

# SECURITY WARNING: don't run with debug turned on in production!
if ENVIRONMENT =="development":
    DEBUG = True
else:
    DEBUG = False


# Static and media files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'api',
    'social_media_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_media_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'social_media_api.wsgi.application'

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'social_media_db',
#        'USER': 'social_media_user',
#        'PASSWORD': 'adminpassword',
#        'HOST': 'localhost',
#        'PORT': '5432',
#    }
#}

# Password validation settings
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Timezone and Language
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
