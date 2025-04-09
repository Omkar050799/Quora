from ..base import *

SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Database settings for app
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

# Application Client-ID and Client-Secret

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SERVER_PROTOCOLS = os.getenv("SERVER_PROTOCOLS")

# Frontend URL
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL") == "True"
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") == "True"

FRONT_END_URL = os.getenv("FRONT_END_URL", "http://127.0.0.1:8000/")
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000/api/v1/")

MEDIA_URL = os.getenv("MEDIA_URL")
MEDIA_ROOT = os.path.join(BASE_DIR, os.getenv("MEDIA_ROOT"))

STATIC_URL = os.getenv("STATIC_URL")
STATIC_ROOT = os.path.join(BASE_DIR, os.getenv("STATIC_ROOT"))

IS_LOCAL = os.getenv("IS_LOCAL") == "True"
S_KEY = os.getenv("S_KEY").encode()

IS_LOCAL = os.getenv("IS_LOCAL") == "True"
