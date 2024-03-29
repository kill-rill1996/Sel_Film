import os
from pathlib import Path

from loguru import logger as loguru_logger

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=False)))

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(" ")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # debug_toolbar
    'debug_toolbar',
    'captcha',

    'films',
    'serials',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # debug_toolbar
    "debug_toolbar.middleware.DebugToolbarMiddleware",

    # error log
    "sel_film.middleware.ErrorLogMiddleware",

]

ROOT_URLCONF = 'sel_film.urls'

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

WSGI_APPLICATION = 'sel_film.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('POSTGRES_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.environ.get('POSTGRES_DB', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.environ.get('POSTGRES_USER', 'user'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'password'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [BASE_DIR / "static"]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# debug_toolbar
INTERNAL_IPS = [
    "127.0.0.1",
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        # 'LOCATION': '/var/tmp/django_cache',
        'LOCATION': os.path.join(BASE_DIR, 'selfilm_cache'),
        'TIMEOUT': 600,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        }
    }
}

# Loguru
from datetime import timedelta
td = timedelta(10)


def search_only(record):
    return record['function'] == 'search'


def select_films_only(record):
    return record['function'] == 'search_films'


def contact_page_only(record):
    return record['function'] == 'contact_page'


loguru_logger.add(os.path.join(BASE_DIR, 'logs/films/logs.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter="films.views", rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/serials/selected_serials.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter="serials.views", rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/warning.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='WARNING', rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/films/search.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter=search_only, rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/send_feedback.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter=contact_page_only, rotation='50 MB', compression='zip')
loguru_logger.add(os.path.join(BASE_DIR, 'logs/films/selected_films.log'), format='{level} {time: HH:mm.ss DD.MM.YYYY} {name} ({function}) {message}', level='INFO', filter=select_films_only, rotation='50 MB', compression='zip')


# Email settings
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = bool(int(os.environ.get('EMAIL_USE_TLS')))
# EMAIL_USE_SSL = bool(int(os.environ.get('EMAIL_USE_SSL')))

# Sentry monitoring
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://4f4d47bea2344baa977fd11f31f7221b@o608832.ingest.sentry.io/6106300",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)


# Captcha
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_USE_SSL = bool(int(os.environ.get('RECAPTCHA_USE_SSL')))
