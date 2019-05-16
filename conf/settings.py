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
from directory_constants import cms
import directory_healthcheck.backends


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
    'investment_support_directory',
    'formtools',
    'notifications',
    'directory_constants',
    'captcha',
    'sorl.thumbnail',
    'directory_components',
    'directory_healthcheck',
]

MIDDLEWARE_CLASSES = [
    'directory_components.middleware.MaintenanceModeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'directory_components.middleware.LocaleQuerystringMiddleware',
    'directory_components.middleware.PersistLocaleMiddleware',
    'directory_components.middleware.ForceDefaultLocale',
    'directory_components.middleware.CountryMiddleware',
    'core.middleware.PrefixUrlMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
]

FEATURE_URL_PREFIX_ENABLED = True
URL_PREFIX_DOMAIN = env.str('URL_PREFIX_DOMAIN')
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
                'core.context_processors.footer_contact_us_link',
                'directory_components.context_processors.analytics',
                'directory_components.context_processors.urls_processor',
                ('directory_components.context_processors.'
                    'header_footer_processor'),
                'directory_components.context_processors.feature_flags',
                'core.context_processors.html_lang_attribute',
                'directory_components.context_processors.cookie_notice',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

VCAP_SERVICES = env.json('VCAP_SERVICES', {})

if 'redis' in VCAP_SERVICES:
    REDIS_URL = VCAP_SERVICES['redis'][0]['credentials']['uri']
else:
    REDIS_URL = env.str('REDIS_URL', '')

if REDIS_URL:
    cache = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': "django_redis.client.DefaultClient",
        }
    }
else:
    cache = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }

CACHES = {
    'default': cache,
    'cms_fallback': cache,
    'api_fallback': cache,
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-LANGUAGE_COOKIE_NAME
LANGUAGE_COOKIE_DEPRECATED_NAME = 'django-language'
# Django's default value for LANGUAGE_COOKIE_DOMAIN is None
LANGUAGE_COOKIE_DOMAIN = env.str('LANGUAGE_COOKIE_DOMAIN', None)

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
    'EXPORT_JOURNEY_ON': False,  # not used in this project
    'INVESTMENT_SUPPORT_DIRECTORY_ON': env.bool(
        'FEATURE_INVESTMENT_SUPPORT_DIRECTORY_ENABLED', False
    ),
    'INTERNATIONAL_CONTACT_LINK_ON': env.bool(
        'FEATURE_INTERNATIONAL_CONTACT_LINK_ENABLED', False
    ),
    'MAINTENANCE_MODE_ON': env.bool('FEATURE_MAINTENANCE_MODE_ENABLED', False),
    'EU_EXIT_BANNER_ON': env.bool(
        'FEATURE_EU_EXIT_BANNER_ENABLED', False
    ),
    'NEWS_SECTION_ON': env.bool('FEATURE_NEWS_SECTION_ENABLED', False),
    'COUNTRY_SELECTOR_ON': env.bool('FEATURE_COUNTRY_SELECTOR_ENABLED', False)
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
THUMBNAIL_KVSTORE = THUMBNAIL_KVSTORE_CLASSES[THUMBNAIL_KVSTORE_CLASS_NAME]
THUMBNAIL_STORAGE = THUMBNAIL_STORAGE_CLASSES[THUMBNAIL_STORAGE_CLASS_NAME]
# Workaround for slow S3
# https://github.com/jazzband/sorl-thumbnail#is-so-slow-in-amazon-s3-
THUMBNAIL_FORCE_OVERWRITE = True

# Redis for thumbnails cache
if REDIS_URL:
    THUMBNAIL_REDIS_URL = REDIS_URL

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
    'DIRECTORY_CMS_API_CLIENT_DEFAULT_TIMEOUT', 2
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
DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME = env.str(
    'DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME', 'Directory'
)
ZENDESK_TICKET_SUBJECT = env.str(
    'ZENDESK_TICKET_SUBJECT', 'Trade Profiles feedback'
)
CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_COMPANY_NOTIFY_TEMPLATE_ID',
    'a0ffc316-09f0-4b28-9af0-86243645efca'
)
CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_SUPPORT_NOTIFY_TEMPLATE_ID',
    '19fc13d1-fcc1-4e3b-a488-244a520742e2'
)
CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID = env.str(
    'CONTACT_ISD_INVESTOR_NOTIFY_TEMPLATE_ID',
    '351e32e9-2e66-4a6f-8b20-a9942f045f1b'
)
CONTACT_ISD_SUPPORT_EMAIL_ADDRESS = env.str(
    'CONTACT_ISD_SUPPORT_EMAIL_ADDRESS', ''
)
# directory client core
DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS = env.int(
    'DIRECTORY_CLIENT_CORE_CACHE_EXPIRE_SECONDS',
    60 * 60 * 24 * 30  # 30 days
)

# directory-components
PRIVACY_COOKIE_DOMAIN = env.str('PRIVACY_COOKIE_DOMAIN')

# Healthcheck
DIRECTORY_HEALTHCHECK_TOKEN = env.str('HEALTH_CHECK_TOKEN')
DIRECTORY_HEALTHCHECK_BACKENDS = [
    directory_healthcheck.backends.APIBackend,
    directory_healthcheck.backends.FormsAPIBackend,
]

# HEADER AND FOOTER LINKS
DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC = env.str(
    'DIRECTORY_CONSTANTS_URL_GREAT_DOMESTIC', ''
)
DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL = env.str(
    'DIRECTORY_CONSTANTS_URL_GREAT_INTERNATIONAL', ''
)
DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES = env.str(
    'DIRECTORY_CONSTANTS_URL_EXPORT_OPPORTUNITIES', ''
)
DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS = env.str(
    'DIRECTORY_CONSTANTS_URL_SELLING_ONLINE_OVERSEAS', ''
)
DIRECTORY_CONSTANTS_URL_EVENTS = env.str(
    'DIRECTORY_CONSTANTS_URL_EVENTS', ''
)
DIRECTORY_CONSTANTS_URL_INVEST = env.str('DIRECTORY_CONSTANTS_URL_INVEST', '')
DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_SUPPLIER', ''
)
DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON = env.str(
    'DIRECTORY_CONSTANTS_URL_SINGLE_SIGN_ON', ''
)
DIRECTORY_CONSTANTS_URL_FIND_A_BUYER = env.str(
    'DIRECTORY_CONSTANTS_URL_FIND_A_BUYER', ''
)

# Settings for email to supplier
CONTACT_SUPPLIER_SUBJECT = env.str(
    'CONTACT_SUPPLIER_SUBJECT',
    'Someone is interested in your Find a Buyer profile'
)
CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS = env.str(
    'CONTACT_INDUSTRY_AGENT_EMAIL_ADDRESS'

)
CONTACT_INDUSTRY_AGENT_TEMPLATE_ID = env.str(
    'CONTACT_INDUSTRY_AGENT_TEMPLATE_ID',
    'a9318bce-7d65-41b2-8d4c-b4a76ba285a2'
)
CONTACT_INDUSTRY_USER_TEMPLATE_ID = env.str(
    'CONTACT_INDUSTRY_USER_TEMPLATE_ID',
    '6a97f783-d246-42ca-be53-26faf3b08e32'
)
CONTACT_INDUSTRY_USER_REPLY_TO_ID = env.str(
    'CONTACT_INDUSTRY_USER_REPLY_TO_ID',
    None
)
