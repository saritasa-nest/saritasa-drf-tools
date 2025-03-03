import pathlib

ALLOWED_HOSTS = ["*"]

# Build paths inside the project like this: BASE_DIR / "subdir"
CONFIG_DIR = pathlib.Path(__file__).resolve()
BASE_DIR = CONFIG_DIR.parent
SECRET_KEY = "TEST"  # noqa: S105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_filters",
    "django_probes",
    "django_extensions",
    "example.app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "example.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
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

WSGI_APPLICATION = "example.wsgi.application"

# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    # Taken from compose.yaml
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 600,
        "USER": "saritasa-s3-tools",
        "NAME": "saritasa-s3-tools",
        "PASSWORD": "postgres",
        "HOST": "postgres",
        "PORT": 5432,
    },
}

AUTH_USER_MODEL = "app.User"

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "saritasa_drf_tools.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "saritasa_drf_tools.django_filters.DjangoFilterBackend",
        "saritasa_drf_tools.filters.OrderingFilterBackend",
        "saritasa_drf_tools.filters.SearchFilterBackend",
    ),
    "DEFAULT_PAGINATION_CLASS": (
        "saritasa_drf_tools.pagination.LimitOffsetPagination"
    ),
    "PAGE_SIZE": 25,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "TEST_REQUEST_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "saritasa_drf_tools.renderers.BrowsableAPIRenderer",
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

SARITASA_DRF_MAX_PAGINATION_SIZE = 100
SARITASA_DRF_FIELD_MAPPING = {
    "django.db.models.TextField": "example.app.api.fields.CustomCharField",
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3.S3Storage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
