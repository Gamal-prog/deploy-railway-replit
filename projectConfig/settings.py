from pathlib import Path
import os

import dj_database_url
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()


def env_bool(name, default=False):
    value = os.environ.get(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    value = os.environ.get(name, default)
    return [item.strip() for item in value.split(",") if item.strip()]


def first_env(*names, default=""):
    for name in names:
        value = os.environ.get(name)
        if value:
            return value.strip()
    return default


SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-demo-key-for-local-and-mvp-hosting",
)

DEBUG = env_bool("DEBUG", default=False)

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,.localhost,.up.railway.app,.railway.app,"
    ".replit.app,.replit.dev,.repl.co,.onrender.com",
)

CSRF_TRUSTED_ORIGINS = env_list(
    "CSRF_TRUSTED_ORIGINS",
    "https://*.up.railway.app,https://*.railway.app,https://*.replit.app,"
    "https://*.replit.dev,https://*.repl.co,https://*.onrender.com",
)

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "projectConfig.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "projectConfig.wsgi.application"


DATABASE_URL = os.environ.get("DATABASE_URL")
PGDATABASE = os.environ.get("PGDATABASE")
PGUSER = os.environ.get("PGUSER")
PGPASSWORD = os.environ.get("PGPASSWORD")
PGHOST = os.environ.get("PGHOST")
PGPORT = os.environ.get("PGPORT", "5432")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=DATABASE_URL.startswith(("postgres://", "postgresql://")),
        )
    }
elif all([PGDATABASE, PGUSER, PGPASSWORD, PGHOST]):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": PGDATABASE,
            "USER": PGUSER,
            "PASSWORD": PGPASSWORD,
            "HOST": PGHOST,
            "PORT": PGPORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


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


LANGUAGE_CODE = "ru-ru"
TIME_ZONE = "Asia/Bishkek"
USE_I18N = True
USE_TZ = True


STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

BUNNY_STREAM_LIBRARY_ID = 703470
BUNNY_STREAM_API_KEY = first_env(
    "BUNNY_STREAM_API_KEY",
    "BUNNY_STREAM_ACCESS_KEY",
    "BUNNY_STREAM_API_READ_ONLY_KEY",
    "BUNNY_API_KEY",
    "BUNNY_ACCESS_KEY",
    "BUNNY_API_READ_ONLY_KEY",
    "API_READ_ONLY_KEY",
    "API-Read-Only",
)
BUNNY_STREAM_API_TIMEOUT = int(os.environ.get("BUNNY_STREAM_API_TIMEOUT", "8"))
BUNNY_STREAM_EMBED_TOKEN_KEY = first_env(
    "BUNNY_STREAM_EMBED_TOKEN_KEY",
    "BUNNY_STREAM_TOKEN_AUTH_KEY",
    "BUNNY_STREAM_TOKEN_SECURITY_KEY",
    "BUNNY_EMBED_TOKEN_KEY",
    "BUNNY_TOKEN_AUTH_KEY",
)
BUNNY_STREAM_EMBED_TOKEN_TTL = int(
    os.environ.get("BUNNY_STREAM_EMBED_TOKEN_TTL", "3600")
)
