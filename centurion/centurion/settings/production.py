from centurion.settings.common import *

DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0', 'localhost']
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'centurion', 
        'USER': 'centurion',
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}