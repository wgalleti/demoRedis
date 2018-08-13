import os
from datetime import timedelta

from decouple import config, Csv
from dj_database_url import parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool, default=False)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv(), default=[])

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_APPS = [
    'corsheaders',
    'rest_framework',
    'rest_auth',
    'rest_framework.authtoken',
    'rest_framework_jwt',
    'django_filters',
    'django_extensions',
    'django_python3_ldap',
    'rest_framework_swagger',
    'django_redis',
    'django_rq',
]

LOCAL_APPS = [
    'integrador',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_APPS + LOCAL_APPS

CORS_ORIGIN_ALLOW_ALL = True

LOGIN_URL = 'rest_framework:login'
LOGOUT_URL = 'rest_framework:logout'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination'
}

REST_USE_JWT = True

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(seconds=30000),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_python3_ldap.auth.LDAPBackend',
)

LDAP_AUTH_URL = config('LDAP_URL')
LDAP_AUTH_USE_TLS = config('LDAP_USE_TLS', default=False, cast=bool)
LDAP_AUTH_SEARCH_BASE = config('LDAP_SEARCH_BASE')
LDAP_AUTH_OBJECT_CLASS = config('LDAP_OBJECT_CLASS')
LDAP_AUTH_USER_FIELDS = {'username': 'sAMAccountName',
                         'first_name': 'givenName',
                         'last_name': 'sn',
                         'email': 'mail', }
LDAP_AUTH_USER_LOOKUP_FIELDS = ('username',)
LDAP_AUTH_CLEAN_USER_DATA = config('LDAP_CLEAN_USER_DATA')
LDAP_AUTH_SYNC_USER_RELATIONS = config('LDAP_SYNC_USER_RELATIONS')
LDAP_AUTH_FORMAT_SEARCH_FILTERS = config('LDAP_FORMAT_SEARCH_FILTERS')
LDAP_AUTH_FORMAT_USERNAME = config('LDAP_FORMAT_USERNAME')
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = config('LDAP_ACTIVE_DIRECTORY_DOMAIN')
LDAP_AUTH_CONNECTION_USERNAME = config('LDAP_CONNECTION_USERNAME')
LDAP_AUTH_CONNECTION_PASSWORD = config('LDAP_CONNECTION_PASSWORD')

EMAIL_BACKEND = config('MAIL_BACKEND')
EMAIL_HOST = config('MAIL_HOST')
DEFAULT_FROM_EMAIL = config('MAIL_DEFAULT_FROM')
SERVER_EMAIL = config('MAIL_SERVER')
EMAIL_HOST_USER = config('MAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('MAIL_HOST_PASSWORD')
EMAIL_PORT = config('MAIL_PORT', cast=int)
EMAIL_USE_TLS = config('MAIL_USE_TLS', cast=bool)

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MAX_ENTRIES': 5000,
        },
    },
    'high': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/2',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'MAX_ENTRIES': 10000,
        },
    },
}

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 0,
        'PASSWORD': '',
        'DEFAULT_TIMEOUT': 360,
    },
    'high': {
        'USE_REDIS_CACHE': 'high',
    },
    'low': {
        'USE_REDIS_CACHE': 'default',
    }
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# DATABASES
DATABASES = dict()
DATABASES['default'] = config('DB_DEFAULT', cast=parse, default=f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}")

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = []

# INTERNATIONALIZATION
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Cuiaba'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# STATIC FILES (CSS, JAVASCRIPT, IMAGES)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA FILES (CSS, JAVASCRIPT, IMAGES)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# LOG
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "rq_console": {
            "format": "%(asctime)s %(message)s",
            "datefmt": "%H:%M:%S",
        },
    },
    "handlers": {
        "rq_console": {
            "level": "DEBUG",
            "class": "rq.utils.ColorizingStreamHandler",
            "formatter": "rq_console",
            "exclude": ["%(asctime)s"],
        },
    },
    'loggers': {
        "rq.worker": {
            "handlers": ["rq_console"],
            "level": "DEBUG"
        },
    }
}
