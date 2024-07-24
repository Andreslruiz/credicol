"""
Django settings for ROM project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = environ.Path(__file__) - 2

ENV = environ.Env()
ENV.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c5(v+#q#f=91@@#s*n+6gz9!fs)&ia_w)m2olssigq6)z)r#2l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = [
    'https://credicol.com.co',
    'http://credicol.com.co',
    'https://www.credicol.com.co',
    'http://www.credicol.com.co',
]

# Configuración para asegurar que las cookies de sesión solo se envíen a través de conexiones seguras
SESSION_COOKIE_SECURE = True

# Configuración para asegurar que las cookies CSRF solo se envíen a través de conexiones seguras
CSRF_COOKIE_SECURE = True


CRISPY_TEMPLATE_PACK = 'bootstrap4'
SITE_URL = ENV.str('SITE_URL', default='http://localhost:8000')
WSSP_KEY = os.getenv('WSSP_API_KEY')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'waffle',
    'crispy_forms',
    'crispy_bootstrap4',
    'common',
    'companies',
    'clientes',
    'productos',
    'simple_history',
    'transacciones',
    'django_q',
    'import_export',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.TimezoneMiddleware',
]

ROOT_URLCONF = 'ROM.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'ROM.wsgi.application'
DATA_UPLOAD_MAX_NUMBER_FIELDS = 20000

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': ENV.db(),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/


TIME_ZONE = 'America/Bogota'
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('../static')
STATICFILES_DIRS = (BASE_DIR('static'),)

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR('../media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


Q_CLUSTER = {
    'name': 'credicol',
    'catch_up': False,
    'orm': 'default',
    'max_attempts': 1,
    'timeout': 2500,
    'recycle': 100,
    'retry': 3000,
}
