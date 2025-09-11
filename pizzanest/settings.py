from pathlib import Path
from decouple import config , Csv
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Key....
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG',cast=bool, default=False)
# Security Settings
CSRF_COOKIE_SECURE = config("CSRF_COOKIE_SECURE", cast=bool, default=False)
SESSION_COOKIE_SECURE = config("SESSION_COOKIE_SECURE", cast=bool, default=False)
SECURE_CONTENT_TYPE_NOSNIFF = config("SECURE_CONTENT_TYPE_NOSNIFF", cast=bool, default=True)
SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", cast=bool, default=False)

# Host
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'account',
    'customer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'account.middleware.CustomLoginRequiredMiddleware', # custom login required
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'account.middleware.UnderConstMiddleware', # underconstruction middleware
]

ROOT_URLCONF = 'pizzanest.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pizzanest.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
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
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
import os
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # where we collect file after deploy

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# media file upload settings.....
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# Email Settings
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

# Session end when close browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

#cookies...
SESSION_COOKIE_AGE = 1800  # seconds   
SESSION_SAVE_EVERY_REQUEST = True  # Reset timer on activity
PASSWORD_RESET_TIMEOUT = 600   # email expire in 10 minutes....



# LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'   # When session will expire then will redirect login


#logging setting for debug....

from pathlib import Path
import logging
from logging.handlers import TimedRotatingFileHandler

BASE_DIR = Path(__file__).resolve().parent.parent

# ensure logs folder exists
os.makedirs(BASE_DIR / "logs", exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",  # Production me DEBUG ke bajaye INFO ya WARNING
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": BASE_DIR / "logs/app.log",
            "when": "midnight",
            "interval": 1,
            "backupCount": 30,   # last 30 days logs
            "formatter": "standard",
            "encoding": "utf-8",
            "delay": True,       # Windows file lock fix
        },
    },
    "loggers": {
        "": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
