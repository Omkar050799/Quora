import os
from dotenv import load_dotenv
from pathlib import Path
from ..base import *

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

# Database settings
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DB_ENGINE"),
        "NAME": os.getenv("DB_NAME"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
    }
}

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SERVER_PROTOCOLS = os.getenv("SERVER_PROTOCOLS")

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"

FRONT_END_URL = os.getenv("FRONT_END_URL")
BASE_URL = os.getenv("BASE_URL")

MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT"))

STATIC_URL = os.getenv("STATIC_URL")
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv("STATIC_ROOT"))

IS_LOCAL = os.getenv("IS_LOCAL") == "True"
S_KEY = os.getenv("S_KEY").encode()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.getenv("LOG_FILE_ERROR"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
        "request_handler": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.getenv("LOG_FILE_ACCESS"),
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["default"],
        "level": "DEBUG",
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["request_handler"],
            "level": "DEBUG",
        },
    },
}

DEFAULT_FROM_EMAIL = 'noreply@quora.in'
