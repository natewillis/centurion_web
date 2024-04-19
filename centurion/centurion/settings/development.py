from centurion.settings.common import *


# Production logging will go into apaches logs
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'scenario': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}
