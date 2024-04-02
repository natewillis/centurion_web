from centurion.settings.common import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'centurion', 
        'USER': 'postgres',
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
        'OPTIONS': {
            'connect_timeout': 60,  # Set the timeout to 60 seconds
            'options': '-c statement_timeout=60000',
        },
    }
}

INTERNAL_IPS = (
    '127.0.0.1',
)