import os
import posixpath
from pathlib import Path

from environs import Env

_env_file_name = os.environ.get('ENV_FILE_NAME')
env = Env()
env.read_env(path=_env_file_name, override=True)


BASE_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = os.path.dirname(BASE_DIR)

SECRET_KEY = env.str('SECRET_KEY', '')

DEBUG = env.int('DEBUG', 1)

ALLOWED_HOSTS = env.str('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split(' ')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # additional libs
    'rest_framework',
    'drf_yasg',
    # local apps
    'mainapp',
    'help',
    'attachment',
]

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mainapp.urls'

TEMPLATES = [
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
]

WSGI_APPLICATION = 'mainapp.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': env.str('SQL_ENGINE'),
        'NAME': env.str('SQL_DATABASE'),
        'USER': env.str('SQL_USER', 'user'),
        'PASSWORD': env.str('SQL_PASSWORD', 'password'),
        'HOST': env.str('SQL_HOST', 'localhost'),
        'PORT': env.str('SQL_PORT', '5432'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = False


_url_prefix = env.str('API_URL_PEFIX', '')
URL_PREFIX = posixpath.join(_url_prefix, '')

MEDIA_URL = posixpath.join(URL_PREFIX, 'media/')
STATIC_URL = posixpath.join(URL_PREFIX, 'static/')

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'mainapp.User'


MAINAPP_PATH = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(MAINAPP_PATH, 'test_data')
TEST_IMAGE = os.path.join(TEST_DATA_PATH, 'jpeg.jpeg')
TEST_PDF = os.path.join(TEST_DATA_PATH, 'pdf.pdf')
