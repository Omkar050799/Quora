PROJECTNAME = "quora"
APPNAME = "quora_app"
(
    """
Django settings for """
    + PROJECTNAME
    + """ project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
)

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.contrib.auth import get_user_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "oauth2_provider",
    "drf_yasg",
    APPNAME,
]

# Middleware

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "quora.middleware.ErrorHandlerMiddleware",
]

# Maintenancemode configuration
IS_MAINTENANCE_MODE = False
MAINTENANCE_IPS = ["127.0.0.1"]

CORS_ORIGIN_ALLOW_ALL = True
ROOT_URLCONF = PROJECTNAME + ".urls"
OTP_LENGTH = 6

# Add template path
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templatesAPPNAME"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

SWAGGER_SETTINGS = {
    "exclude_url_names": [],
    "exclude_namespaces": ["internal_apis"],
    "USE_SESSION_AUTH": True,
    "resource_access_handler": None,
    "SECURITY_DEFINITIONS": {
        "token": {"type": "apiKey", "in": "header", "name": "Authorization"}
    },
}

WSGI_APPLICATION = f'{PROJECTNAME}.wsgi.application'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "oauth2_provider.contrib.rest_framework.OAuth2Authentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/min",        # Anonymous users
        "user": "20/min",        # Authenticated users
        "login": "10/min",       # Login attempts
        "file_upload": "8/min",  # File upload limit
        "strict": "15/min",      # Strictly limited API usage
        "medium": "40/min",      # Medium usage
        "lite": "60/min",        # Lightly restricted
        "extra_lite": "80/min",  # Minimal restrictions
    },
}

AUTHENTICATION_BACKENDS = (
    APPNAME + ".models.EmailOrUsernameModelBackend",
    "django.contrib.auth.backends.ModelBackend",
)

AUTH_USER_MODEL = APPNAME + ".User"

# Acces token scope and expire seconds
OAUTH2_PROVIDER = {
    "SCOPES": {"read": "Read scope"},
    "ACCESS_TOKEN_EXPIRE_SECONDS": 36000,
}

PAGE_SIZE = 10

# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR + "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# master roles
GRP_SUPER_ADMIN = 1

HEADERS = "AE698wLwHGPLvtuzF46V4P2h4yh3ru2MmkBKpsEA7bzQSHjQ3F"

PAGE_SIZE = 10

# Use nose to run all tests
TEST_RUNNER = "django_nose.NoseTestSuiteRunner"

# Tell nose to measure coverage on the 'foo' and 'bar' apps
NOSE_ARGS = [
    "--with-coverage",
    "--cover-package=quora_app",
    "--verbosity=3",
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

# Celery Settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "memory://")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "memory://")
CELERY_RESULT_PERSISTENT = os.getenv("CELERY_RESULT_PERSISTENT", "False")
CELERY_ACCEPT_CONTENT = [os.getenv("CELERY_ACCEPT_CONTENT", "json")]
CELERY_TASK_SERIALIZER = os.getenv("CELERY_TASK_SERIALIZER", "json")
CELERY_RESULT_SERIALIZER = os.getenv("CELERY_RESULT_SERIALIZER", "json")
CELERY_TIMEZONE = os.getenv("CELERY_TIMEZONE", "UTC")
