"""
Django settings for picbackend project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

# Use 12factor inspired environment variables or from a file
import environ
env = environ.Env(DEBUG=(bool, True),)

# Ideally move env file should be outside the git repo
# i.e. BASE_DIR.parent.parent
env_file = os.path.join(os.path.dirname(__file__), 'local.env')
if os.path.exists(env_file):
    environ.Env.read_env(str(env_file))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

GOOGLE_OAUTH2_CLIENT_SECRETS_JSON = os.path.join(os.path.dirname(__file__), 'client_secret.json')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'picmodels',
    "django_extensions",
)

MIDDLEWARE_CLASSES = (
    'picbackend.django-crossdomainxhr-middleware.XsSharing',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'picbackend.urls'

# sets template directory to root/templates
PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates'),],
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

WSGI_APPLICATION = 'picbackend.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's!=a^t83cuz95n16m6s0*-r!ad%m3s8)t_tw9u0=4928vu1f$i'

"""
This section of code configures the application for the Heroku environment.
The dj-database-url module will parse the value of the DATABASE_URL environment variable
and convert them to something Django can understand. dj-database-url must be in requirements.txt.
"""
# Parse database configuration from $DATABASE_URL
import dj_database_url

# DATABASES['default'] = dj_database_url.config(
#     default='postgres://ngklalieajpptd:Day5uAny5L-cI0OB3L2nUmfHhh@ec2-54-197-224-173.compute-1.amazonaws.com:5432/dehaud8hlr9iqq')
DATABASES = {
    'default': dj_database_url.config()
    }
# DATABASES['default'] = dj_database_url.config('postgres://Kirabee:n1ggmag3@localhost:5432/mydb')

# # Enable Persistent Connections
# DATABASES['default']['CONN_MAX_AGE'] = 500
""""""

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# If all url attempts are exhausted and site about to return
# 404, append a slash to the end of url and try again
APPEND_SLASH = True

STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures'),
)

