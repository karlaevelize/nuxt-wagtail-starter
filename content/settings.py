import json
import os

from configparser import ConfigParser
from pathlib import Path

# Default and local config files can be found here
PROJECT_DIR = Path(__file__).resolve().parent

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = PROJECT_DIR.parent

config = ConfigParser(converters={"literal": json.loads}, interpolation=None)
config.read(
    [
        os.environ.get("APP_SETTINGS", PROJECT_DIR / "local.ini"),
        PROJECT_DIR / "local.ini",
    ]
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.getliteral("app", "secret_key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.getboolean("app", "debug", fallback=False)

ALLOWED_HOSTS = config.getliteral("app", "allowed_hosts")

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Security settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_CONTENT_TYPE_NOSNIFF = True  # Adds 'X-Content-Type-Options: nosniff' header
SECURE_BROWSER_XSS_FILTER = True  # Adds 'X-XSS-Protection: 1; mode=block' header
X_FRAME_OPTIONS = "DENY"  # Don't allow this site to be framed
SECURE_REFERRER_POLICY = (
    "strict-origin, strict-origin-when-cross-origin"  # Adds 'Referrer-Policy' header
)
SILENCED_SYSTEM_CHECKS = [
    # These are all handled by nginx, so Django doesn't need to worry about them
    "security.W004",  # You have not set a value for the SECURE_HSTS_SECONDS setting
    "security.W008",  # SECURE_SSL_REDIRECT setting is not set to True
    *config.getliteral("app", "silenced_system_checks", fallback=[]),
]

# Application definition

INSTALLED_APPS = [
    "content.home",
    "content.mysite",
    "content.accounts",
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.admin",
    "wagtail",
    "wagtail.api.v2",
    "wagtail_headless_preview",
    "modelcluster",
    "taggit",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
]

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "content.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR / "templates"),
        ],
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

WSGI_APPLICATION = "content.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": config.getliteral("app", "db_host", fallback=""),
        "NAME": config.getliteral("app", "db_name"),
        "USER": config.getliteral("app", "db_user"),
        "OPTIONS": {
            "passfile": Path("~/.pgpass").expanduser(),
        },
    }
}

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# When upgrading existing projects use django.db.models.AutoField
# to avoid changing the primary key of existing models
# DEFAULT_AUTO_FIELD = "django.db.models.AutoField"  # noqa: ERA001

# When creating new projects django.db.models.BigAutoField is preferred
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Custom user model
AUTH_USER_MODEL = "accounts.User"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "nl-nl"

TIME_ZONE = "Europe/Amsterdam"

USE_I18N = True

USE_TZ = True

# Media files (user uploads)

MEDIA_URL = "/media/"

if DEBUG:
    # MEDIA_ROOT defaults to BASE_DIR/media/ in debug mode
    MEDIA_ROOT = config.getliteral(
        "app", "media_root", fallback=str(BASE_DIR / "media")
    )
else:
    # Require MEDIA_ROOT to be configured
    MEDIA_ROOT = config.getliteral("app", "media_root")

# File upload permissions
# https://docs.djangoproject.com/en/4.2/ref/settings/#file-upload-permissions
FILE_UPLOAD_PERMISSIONS = 0o644

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_DIRS = []

if DEBUG:
    # STATIC_ROOT defaults to BASE_DIR/static/ in debug mode
    STATIC_ROOT = config.getliteral(
        "app", "static_root", fallback=str(BASE_DIR / "static")
    )
else:
    # Require STATIC_ROOT to be configured
    STATIC_ROOT = config.getliteral("app", "static_root")


# Email backends
EMAIL_BANDIT = config.getliteral("app", "email_bandit", fallback=False)

if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_HOST = config.getliteral("app", "email_host", fallback="localhost")
    EMAIL_PORT = config.getliteral("app", "email_port", fallback=25)
    EMAIL_HOST_USER = config.getliteral("app", "email_host_user", fallback="")
    EMAIL_HOST_PASSWORD = config.getliteral("app", "email_host_password", fallback="")
    EMAIL_USE_TLS = config.getliteral("app", "email_use_tls", fallback=False)
    EMAIL_USE_SSL = config.getliteral("app", "email_use_ssl", fallback=False)

    if EMAIL_BANDIT:
        EMAIL_BACKEND = "bandit.backends.smtp.HijackSMTPBackend"
        BANDIT_EMAIL = config.getliteral("app", "bandit_email")
        BANDIT_WHITELIST = config.getliteral(
            "app", "bandit_whitelist", fallback=["leukeleu.nl"]
        )

DEFAULT_FROM_EMAIL = config.getliteral("app", "default_from_email")


# Wagtail

WAGTAIL_ENABLE_UPDATE_CHECK = DEBUG

WAGTAIL_SITE_NAME = config.getliteral(
    "app",
    "wagtail_site_name",
    fallback="content",
)

WAGTAILADMIN_BASE_URL = config.getliteral("app", "wagtailadmin_base_url")

WAGTAILIMAGES_EXTENSIONS = ["gif", "jpg", "jpeg", "png", "webp", "svg"]

# Reverse the default case-sensitive handling of tags
TAGGIT_CASE_INSENSITIVE = True

# Allow all origins for CORS
CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [f"https://{WAGTAILADMIN_BASE_URL}"]

WAGTAIL_HEADLESS_PREVIEW = {
    "CLIENT_URLS": {
        "default": "{SITE_ROOT_URL}/@preview/",
    },
}
