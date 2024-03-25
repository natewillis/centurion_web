from centurion.settings.common import *

DEBUG = False
ALLOWED_HOSTS = ['0.0.0.0', 'localhost', 'centuriondevelopment.net', 'www.centuriondevelopment.net', '64.23.128.107']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'centurion', 
        'USER': 'centurion',
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}