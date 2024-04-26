from .settings import *
ALLOWED_HOSTS = ["*"]
SITE_URL = ENV.str('SITE_URL', default='https://credicol.com.co')
DEBUG = True
