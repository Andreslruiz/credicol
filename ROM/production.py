from .settings import *


ALLOWED_HOSTS = ["*"]
SITE_URL = ENV.str('SITE_URL', default='https://credicol.com.co')
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'credicol',
        'USER': 'postgres',
        'PASSWORD': '25335286525Andr',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}
