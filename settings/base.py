import os
import logging.config

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

INSTALLED_APPS = [
    'freedomlink'
]

IMPORT_ACCOUNT_EMAIL = 'test_sup@example.com'
SPREADSHEET_NAME = 'FreedomLink Snapshot'
STORY_WORKSHEET_NAME = 'Stories'
STORY_EXPORT_WORKSHEET_NAME = 'Sent Stories'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'db',
        'NAME': 'postres',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'PORT': 5432,
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
              '%(levelname)s|%(asctime)s|%(name)s[%(lineno)s-%(funcName)s]>> %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'dreamsuite.log',
            'formatter':'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'export_import': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

logging.config.dictConfig(LOGGING)
