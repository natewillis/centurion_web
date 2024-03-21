from centurion.settings.common import *


GDAL_LIBRARY_PATH = env("GDAL_LIBRARY_PATH")

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'centurion', 
        'USER': 'postgres',
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': '127.0.0.1', 
        'PORT': '5432',
    }
}