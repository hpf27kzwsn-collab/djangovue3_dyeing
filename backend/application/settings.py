import os
from .plugins import APPS
from .database_config import database_settings
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(os.environ.get('DJANGO_BASE_DIR', Path(__file__).resolve().parent.parent))
WEB_DIR = Path(os.environ.get('DJANGO_WEB_DIR', BASE_DIR.parent / 'web' / 'dist'))
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'djangovue3-local-development-signing-key')
DEBUG = os.environ.get('DJANGO_DEBUG', '1') == '1'
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
INSTALLED_APPS = [
    'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions',
    'django.contrib.messages', 'django.contrib.staticfiles',
    'rest_framework', 'django_filters', 'corsheaders', 'drf_spectacular', 'captcha',
    'django_celery_beat', 'django_celery_results', 'system',
] + APPS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware', 'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware', 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware', 'system.middleware.OperationLoggingMiddleware',
]
ROOT_URLCONF = 'application.urls'
AUTH_USER_MODEL = 'system.Users'
DATABASES = {'default': database_settings(BASE_DIR)}
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates',
              'DIRS': [WEB_DIR], 'APP_DIRS': True,
              'OPTIONS': {'context_processors': ['django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'application.wsgi.application'
ASGI_APPLICATION = 'application.asgi.application'
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_PASSWORD_VALIDATORS = []
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [WEB_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
CORS_ALLOWED_ORIGINS = ['http://localhost:8080', 'http://127.0.0.1:8080']
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication', 'rest_framework.authentication.SessionAuthentication'],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_PAGINATION_CLASS': 'core.responses.Pagination',
    'DEFAULT_SCHEMA_CLASS': 'core.schema.SystemSchema',
    'EXCEPTION_HANDLER': 'core.responses.exception_handler',
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
}
SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(days=1), 'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
              'AUTH_HEADER_TYPES': ('Bearer',), 'ROTATE_REFRESH_TOKENS': True}
SPECTACULAR_SETTINGS = {'TITLE': 'djangovue3 API', 'VERSION': '1.0.0', 'COMPONENT_SPLIT_REQUEST': True}
CAPTCHA_IMAGE_SIZE = (160, 46)
CAPTCHA_LENGTH = 4
REDIS_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6389')
CELERY_BROKER_URL = REDIS_URL + '/3'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BEAT_SYNC_EVERY = 1
CELERY_TIMEZONE = TIME_ZONE
CELERY_IMPORTS = ('system.tasks',)
API_LOG_ENABLE = True
API_LOG_METHODS = ['POST', 'PUT', 'PATCH', 'DELETE']
