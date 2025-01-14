"""
Django settings for rqg project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

from configurations import Configuration, values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PREFIX = None


class Default(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.Value(default='django-insecure-juz0lhy$3yy4h39r&a_**@+orzkz(w%959m!!pr)ov^8@y1#yd',
                              environ_prefix=ENV_PREFIX)

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False, environ_prefix=ENV_PREFIX)
    DEBUG_TOOLBAR_ENABLED = values.BooleanValue(False, environ_prefix=ENV_PREFIX)

    ALLOWED_HOSTS = values.ListValue(['*'], environ=False)

    # Application definition

    @property
    def INSTALLED_APPS(self) -> list[str]:  # noqa
        return [
            # Django Unfold admin
            'unfold',  # before django.contrib.admin
            'unfold.contrib.filters',  # optional, if special filters are needed
            'unfold.contrib.forms',  # optional, if special form elements are needed
            'unfold.contrib.inlines',  # optional, if special inlines are needed
            'unfold.contrib.import_export',  # optional, if django-import-export package is used
            'unfold.contrib.guardian',  # optional, if django-guardian package is used
            'unfold.contrib.simple_history',  # optional, if django-simple-history package is used
            # Django default
            'django.contrib.admin',  # required
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            # Third-party apps
            'corsheaders',
            'django_extensions',
            'drf_spectacular',
            'drf_spectacular_sidecar',
            'rest_framework',
            # Custom apps
            'contrib',
            'quotes',
        ]

    @property
    def MIDDLEWARE(self) -> list[str]:  # noqa
        return [
            'corsheaders.middleware.CorsMiddleware',
            'django.middleware.security.SecurityMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

    CORS_ALLOWED_ORIGINS = values.ListValue(
        [
            'http://localhost:3000',
            'http://0.0.0.0:3000',
        ],
        environ=False,
    )
    ROOT_URLCONF = values.Value(default='rqg.urls', environ=False)

    TEMPLATES = values.ListValue(
        [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
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
        ],
        environ=False,
    )

    WSGI_APPLICATION = values.Value(default='rqg.wsgi.application', environ=False)

    # Database
    # https://docs.djangoproject.com/en/5.1/ref/settings/#databases

    @property
    def DATABASES(self) -> dict[str, dict[str, str | Path]]:  # noqa
        return {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.getenv(key='POSTGRES_DB', default='postgres'),
                'USER': os.getenv(key='POSTGRES_USER', default='postgres'),
                'PASSWORD': os.getenv(key='POSTGRES_PASSWORD', default='postgres'),
                'HOST': 'db',  # Service name from docker-compose
                'PORT': '5432',  # Default PostgreSQL port (as specified in docker-compose)
            }
        }

    # Password validation
    # https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = values.ListValue(
        [
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
        ],
        environ=False,
    )

    # Internationalization
    # https://docs.djangoproject.com/en/5.1/topics/i18n/

    LANGUAGE_CODE = values.Value(default='en-us', environ=False)

    TIME_ZONE = values.Value(default='Europe/Brussels', environ=False)

    USE_I18N = values.BooleanValue(True, environ=False)

    USE_TZ = values.BooleanValue(True, environ=False)

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/5.1/howto/static-files/

    @property
    def STATIC_ROOT(self) -> Path:  # noqa
        return BASE_DIR / '../static'

    @property
    def MEDIA_ROOT(self) -> Path:  # noqa
        return BASE_DIR / '../media'

    STATIC_URL = values.Value(default='/static/', environ_prefix=ENV_PREFIX)
    MEDIA_URL = values.Value(default='/media/', environ_prefix=ENV_PREFIX)

    # Default primary key field type
    # https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = values.Value(default='django.db.models.BigAutoField', environ=False)

    LOGGING = values.DictValue(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'verbose': {
                    'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                    'style': '{',
                },
                'simple': {
                    'format': '{levelname} {message}',
                    'style': '{',
                },
            },
            'handlers': {
                'console': {
                    'level': 'INFO',
                    'class': 'logging.StreamHandler',
                    'formatter': 'simple',
                },
                'file': {
                    'level': 'ERROR',
                    'class': 'logging.FileHandler',
                    'filename': 'errors.log',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'django': {
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'contrib': {  # Contrib app
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
                'quotes': {  # Quotes app
                    'handlers': ['console', 'file'],
                    'level': 'DEBUG',
                    'propagate': True,
                },
            },
        }
    )

    # Django REST Framework (@see https://www.django-rest-framework.org/tutorial/quickstart/)
    @property
    def REST_FRAMEWORK(self) -> dict[str, any]:  # noqa
        return {
            'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
            'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
            'PAGE_SIZE': 10
        }

    @property
    def SPECTACULAR_SETTINGS(self) -> dict[str, any]:  # noqa
        return {
            'TITLE': 'Random quote generator API',
            'DESCRIPTION': 'API to get quotes',
            'VERSION': '1.0.0',
            'SERVE_INCLUDE_SCHEMA': False,
            'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
            'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
            'REDOC_DIST': 'SIDECAR',
        }

    # Unsplash API
    UNSPLASH_API_CLIENT_ID = os.getenv(key='UNSPLASH_API_CLIENT_ID')

    # API Ninjas
    APININJAS_API_KEY = os.getenv(key='APININJAS_API_KEY')
