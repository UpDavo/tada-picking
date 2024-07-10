import os
from pathlib import Path
from environ import Env

env = Env()
Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-892+#0ln#pl$d0c^vzdr))($43p@-x4&-zt-e51hhj&4qn&76%'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
if env.str('PROD') == 'True':
    DEBUG = False


ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['http://*', 'https://*']
X_FRAME_OPTIONS = 'ALLOWALL'
CORS_ALLOW_ALL_ORIGINS = True

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'dashboard',
    'store',
    'accounts',
    'corsheaders',
    'livereload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'livereload.middleware.LiveReloadScript',
]

ROOT_URLCONF = 'clubtada.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context.context_processors.drawer'
            ],
        },
    },
]

WSGI_APPLICATION = 'clubtada.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':  env.str('DATABASE_NAME_LOCAL'),
        'USER':  env.str('DATABASE_USER_LOCAL'),
        'PASSWORD':  env.str('DATABASE_PASSWORD_LOCAL'),
        'HOST':  env.str('DATABASE_HOST_LOCAL'),
        'PORT': '',
    }
}

if env.str('PROD') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str('DATABASE_NAME'),
            'USER': env.str('DATABASE_USER'),
            'PASSWORD': env.str('DATABASE_PASSWORD'),
            'HOST': env.str('DATABASE_HOST'),
            'PORT': env.str('DATABASE_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


MEDIA_PATH = os.path.abspath(os.path.dirname(__name__))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(MEDIA_PATH, 'media')


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(MEDIA_PATH, 'static'),
    os.path.join(MEDIA_PATH, 'media')
]
STATIC_ROOT = os.path.join(MEDIA_PATH, 'local-cdn', 'static')

# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Set custom user model
AUTH_USER_MODEL = 'core.user'

LOCAL = False
LOGIN = 'accounts:login'
NOT_ALLOWED = 'dashboard:notAllowed'

# S3 Config
# AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
# AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
# #
# EMAIL_SUBJECT_PREFIX = "[Development] -"
# EMAIL_HOST = 'localhost'
# EMAIL_HOST_USER = ''
# EMAIL_HOST_PASSWORD = ''
# EMAIL_PORT = 1025
# EMAIL_USE_TLS = False

# EMAIL_SUBJECT_PREFIX = "[Desarrollo] -"
# EMAIL_HOST = env('EMAIL_HOST')
# EMAIL_HOST_USER = env('EMAIL_HOST_USER')
# DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
# EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = env('EMAIL_PORT')
# EMAIL_USE_SSL = env('EMAIL_USE_SSL')

# SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True


# BASE_URL = 'http://localhost:8000'
