'''
Django settings for ui project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
'''

import os

import environ
from directory_constants.constants import cms

env = environ.Env()
env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_ROOT)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

# As the app is running behind a host-based router supplied by Heroku or other
# PaaS, we can open ALLOWED_HOSTS
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'raven.contrib.django.raven_compat',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'enrolment',
    'company',
    'core',
    'industry',
    'formtools',
    'notifications',
    'directory_constants',
    'captcha',
    'sorl.thumbnail',
    'directory_components',
    'export_elements',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.LocaleQuerystringMiddleware',
    'core.middleware.PersistLocaleMiddleware',
    'core.middleware.ForceDefaultLocale',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'directory_components.middleware.RobotsIndexControlHeaderMiddlware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'core.context_processors.subscribe_form',
                'core.context_processors.lead_generation_form',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.urls_processor',
                ('directory_components.context_processors.'
                    'header_footer_processor'),
                'directory_components.context_processors.feature_flags',
                'core.context_processors.html_lang_attribute',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'


# # Database
# hard to get rid of this
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        # 'LOCATION': 'unique-snowflake',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# https://github.com/django/django/blob/master/django/conf/locale/__init__.py
LANGUAGES = [
    ('en-gb', 'English'),               # English
    ('de', 'Deutsch'),                  # German
    ('ja', '日本語'),                    # Japanese
    ('zh-hans', '简体中文'),             # Simplified Chinese
    ('fr', 'Français'),                 # French
    ('es', 'español'),                  # Spanish
    ('pt', 'Português'),                # Portuguese
    ('pt-br', 'Português Brasileiro'),  # Portuguese (Brazilian)
    ('ar', 'العربيّة'),                 # Arabic
    ('ru', 'Русский'),                  # Russian
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

FEATURE_FLAGS = {
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    'SEARCH_ENGINE_INDEXING_OFF': env.bool(
        'FEATURE_SEARCH_ENGINE_INDEXING_DISABLED', False
    ),
    'DIRECTORY_FORMS_API_ON': env.bool(
        'FEATURE_DIRECTORY_FORMS_API_ENABLED', False
    ),
}


# needed only for dev local storage
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Static files served with Whitenoise and AWS Cloudfront
# http://whitenoise.evans.io/en/stable/django.html#instructions-for-amazon-cloudfront
# http://whitenoise.evans.io/en/stable/django.html#restricting-cloudfront-to-static-files
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_HOST = env.str('STATIC_HOST', '')
STATIC_URL = STATIC_HOST + '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Logging for development
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True,
            },
            '': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
else:
    # Sentry logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': (
                    'raven.contrib.django.raven_compat.handlers.SentryHandler'
                ),
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }


ANALYTICS_ID = env.str('ANALYTICS_ID', '')

SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', True)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', 16070400)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Sentry
RAVEN_CONFIG = {
    'dsn': env.str('SENTRY_DSN', ''),
    'processors': (
        'raven.processors.SanitizePasswordsProcessor',
        'core.sentry_processors.SanitizeEmailMessagesProcessor',
    )
}

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', True)

SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True

# Google Recaptcha
RECAPTCHA_PUBLIC_KEY = env.str('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = env.str('RECAPTCHA_PRIVATE_KEY')
# NOCAPTCHA = True turns on version 2 of recaptcha
NOCAPTCHA = os.getenv('NOCAPTCHA') != 'false'

# Google tag manager
GOOGLE_TAG_MANAGER_ID = env.str('GOOGLE_TAG_MANAGER_ID', '')
GOOGLE_TAG_MANAGER_ENV = env.str('GOOGLE_TAG_MANAGER_ENV', '')
UTM_COOKIE_DOMAIN = env.str('UTM_COOKIE_DOMAIN')

# Zendesk
ZENDESK_SUBDOMAIN = env.str('ZENDESK_SUBDOMAIN')
ZENDESK_TOKEN = env.str('ZENDESK_TOKEN')
ZENDESK_EMAIL = env.str('ZENDESK_EMAIL')
ZENDESK_TICKET_SUBJECT = env.str(
    'ZENDESK_TICKET_SUBJECT', 'Trade Profiles feedback'
)

# Sorl-thumbnail
THUMBNAIL_FORMAT = 'PNG'
THUMBNAIL_STORAGE_CLASS_NAME = env.str('THUMBNAIL_STORAGE_CLASS_NAME', 's3')
THUMBNAIL_KVSTORE_CLASS_NAME = env.str(
    'THUMBNAIL_KVSTORE_CLASS_NAME', 'redis'
)
THUMBNAIL_STORAGE_CLASSES = {
    's3': 'storages.backends.s3boto3.S3Boto3Storage',
    'local-storage': 'django.core.files.storage.FileSystemStorage',
}
THUMBNAIL_KVSTORE_CLASSES = {
    'redis': 'sorl.thumbnail.kvstores.redis_kvstore.KVStore',
    'dummy': 'sorl.thumbnail.kvstores.dbm_kvstore.KVStore',
}
THUMBNAIL_DEBUG = DEBUG
TEMPLATE_DEBUG = DEBUG
THUMBNAIL_KVSTORE = THUMBNAIL_KVSTORE_CLASSES[THUMBNAIL_KVSTORE_CLASS_NAME]
THUMBNAIL_STORAGE = THUMBNAIL_STORAGE_CLASSES[THUMBNAIL_STORAGE_CLASS_NAME]
# Workaround for slow S3
# https://github.com/jazzband/sorl-thumbnail#is-so-slow-in-amazon-s3-
THUMBNAIL_FORCE_OVERWRITE = True

# Redis for thumbnails cache
if os.getenv('REDIS_URL'):
    THUMBNAIL_REDIS_URL = env.str('REDIS_URL')

# django-storages for thumbnails
AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME', '')
AWS_DEFAULT_ACL = 'public-read'
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_ENCRYPTION = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_CUSTOM_DOMAIN = env.str('AWS_S3_CUSTOM_DOMAIN', '')
AWS_S3_REGION_NAME = env.str('AWS_S3_REGION_NAME', 'eu-west-1')
AWS_S3_URL_PROTOCOL = env.str('AWS_S3_URL_PROTOCOL', 'https:')
# Needed for new AWS regions
# https://github.com/jschneier/django-storages/issues/203
AWS_S3_SIGNATURE_VERSION = env.str('AWS_S3_SIGNATURE_VERSION', 's3v4')
AWS_QUERYSTRING_AUTH = env.bool('AWS_QUERYSTRING_AUTH', False)
S3_USE_SIGV4 = env.bool('S3_USE_SIGV4', True)
AWS_S3_HOST = env.str('AWS_S3_HOST', 's3.eu-west-1.amazonaws.com')

# directory CMS client
DIRECTORY_CMS_API_CLIENT_BASE_URL = env.str(
    'DIRECTORY_CMS_API_CLIENT_BASE_URL'
)
DIRECTORY_CMS_API_CLIENT_API_KEY = env.str('DIRECTORY_CMS_API_CLIENT_API_KEY')
DIRECTORY_CMS_API_CLIENT_SENDER_ID = env.str(
    'DIRECTORY_CMS_API_CLIENT_SENDER_ID', 'directory'
)
DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT', 15
)
DIRECTORY_CMS_API_CLIENT_SERVICE_NAME = cms.FIND_A_SUPPLIER

# directory API client
DIRECTORY_API_CLIENT_BASE_URL = env.str('DIRECTORY_API_CLIENT_BASE_URL')
DIRECTORY_API_CLIENT_API_KEY = env.str('DIRECTORY_API_CLIENT_API_KEY')
DIRECTORY_API_CLIENT_SENDER_ID = env.str(
    'DIRECTORY_API_CLIENT_SENDER_ID', 'directory'
)
DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_API_CLIENT_DEFAULT_TIMEOUT', 15
)

# directory forms api client
DIRECTORY_FORMS_API_BASE_URL = env.str('DIRECTORY_FORMS_API_BASE_URL')
DIRECTORY_FORMS_API_API_KEY = env.str('DIRECTORY_FORMS_API_API_KEY')
DIRECTORY_FORMS_API_SENDER_ID = env.str('DIRECTORY_FORMS_API_SENDER_ID')
DIRECTORY_FORMS_API_DEFAULT_TIMEOUT = env.int(
    'DIRECTORY_API_FORMS_DEFAULT_TIMEOUT', 5
)
DIRECTORY_FORMS_API_NAMESPACE = 'find-a-supplier'
