"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import environ
import psycopg2  # pip install psycopg2 and uncomment
# from django.core.checks import Debug

env = environ.Env(
    DEBUG=(bool, False),  # Not necessarily, but recommended
    POSTGRES=(bool, True),  # Not necessarily, but recommended
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = [env("ALLOWED_HOST_1"), env("ALLOWED_HOST_2")]


# Application definition

INSTALLED_APPS = [
    # "admin_interface",  # Added to change admin panel theme, if comment - standard theme
    # "colorfield",  # Added to change admin panel theme, if comment - standard theme
    "debug_toolbar",  # Added

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3-rd apps
    "rest_framework",  # Added for DjangoRestFramework
    "drf_yasg",  # Added for SWAGER

    # local apps
    "apps.todo.apps.TodoConfig",  # Added
    "apps.user.apps.UserConfig",  # Added
    "apps.api.apps.ApiConfig",  # Added
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",  # Added
]

ROOT_URLCONF = 'config.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates",    # Added
                 BASE_DIR / "apps/todo/templates",
                 BASE_DIR / "apps/todo/forms_templates",
                 BASE_DIR / "apps/user/templates",
                 BASE_DIR / "apps/user/forms_templates/",
                 ],  # Added
        # 'DIRS': ["templates", "apps/todo/templates", "apps/todo/forms_templates"],
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


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if env("POSTGRES"):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env('DB_NAME_POS'),
            'USER': env('DB_USER_POS'),
            'PASSWORD': env('DB_PASSWORD_POS'),
            'HOST': env('DB_HOST_POS'),
            'PORT': env('DB_PORT_POS'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'  # 'Poland' - for the Poland for example, not UTC+1

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, "apps", "todo", "static"),  # additional dirs with static files
#     os.path.join(BASE_DIR, "apps", "user", "static"),  # additional dirs with static files
# ]

STATIC_URL = "static/"  # =<each_app_dir>/static - apps dirs, where finder will find static files
STATIC_ROOT = os.path.join(BASE_DIR, "static")  # =<root_proj_dir>/static - where all collected static files will be collected

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",  # Standard AUTH.MODELS django auth by username, if not -> next Backend
    "apps.user.authentications.CustomEmailAuthenticationBackend",  # Custom auth by email
    ]

AUTH_USER_MODEL = 'user.CustomUser'
