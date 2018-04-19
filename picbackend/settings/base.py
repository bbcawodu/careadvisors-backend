"""
Django settings for picbackend project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""


import os
import dj_database_url
import environ


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

# Use 12factor inspired environment variables or from a file
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
    'picbackend',
    'picmodels',
    "django_extensions",
    'corsheaders',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsPostCsrfMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'picbackend.middleware.CsrfHeaderMiddleware'
)

SECURE_SSL_REDIRECT = True # https://docs.djangoproject.com/en/2.0/ref/settings/#secure-ssl-redirect
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CORS_ORIGIN_ALLOW_ALL = False

CORS_ALLOW_CREDENTIALS = True
CORS_REPLACE_HTTPS_REFERER = True

# sets Access-Control-Expose-Headers response header
CORS_EXPOSE_HEADERS = [
    'X-CSRFTOKEN'
]

CORS_ORIGIN_WHITELIST = (
    "google.com",
    "pic-reporting-system.herokuapp.com",
    "navigatornetwork.org",
    "patient-assist-backend.herokuapp.com",
    "dashboard-console-demo.herokuapp.com",
    "dashboard-console-demo.care-advisors.com",
)

CSRF_TRUSTED_ORIGINS = (
    "google.com",
    "pic-reporting-system.herokuapp.com",
    "navigatornetwork.org",
    "patient-assist-backend.herokuapp.com",
    "dashboard-console-demo.herokuapp.com",
    "dashboard-console-demo.care-advisors.com",
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

ROOT_URLCONF = 'picbackend.urls'

# sets template directory to root/templates
PROJECT_DIR = os.path.dirname(__file__)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
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

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's!=a^t83cuz95n16m6s0*-r!ad%m3s8)t_tw9u0=4928vu1f$i'

"""
This section of code configures the application for the Heroku environment.
The dj-database-url module will parse the value of the DATABASE_URL environment variable
and convert them to something Django can understand. dj-database-url must be in requirements.txt.
"""
# Parse database configuration from $DATABASE_URL
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'

# MEDIA_ROOT is the folder where every files uploaded with an FileField will go
# MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
# MEDIA_URL = '/media/'


# Tell django-storages that when coming up with the URL for an item in S3 storage, keep
# it simple - just use this domain plus the path. (If this isn't set, things get complicated).
# This controls how the `static` template tag from `staticfiles` gets expanded, if you're using it.
# We also use it in the next setting.
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
# AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
# AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Tell the staticfiles app to use S3Boto storage when writing the collected static files (when
# you run `collectstatic`).
# STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# STATICFILES_LOCATION = 'static'
# STATICFILES_STORAGE = 'custom_storages.StaticStorage'

# This is used by the `static` template tag from `static`, if you're using that. Or if anything else
# refers directly to STATIC_URL. So it's safest to always set it.
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, STATICFILES_LOCATION)

MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'custom_storages.MediaStorage'
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
DEFAULT_STAFF_PIC_URL = 'staff_pics/None/default_staff_image.jpg'
DEFAULT_CTA_PIC_URL = 'call_to_actions/None/default_cta_image.jpg'
DEFAULT_CARRIER_SAMPLE_ID_CARD_URL = 'carrier_sample_id_cards/None/default_sample_id_card_image.jpg'


# Chartio Settings
CHARTIO_ORG_SECRET = os.environ['CHARTIO_ORG_SECRET']
CHARTIO_BASE_URL = os.environ['CHARTIO_BASE_URL']
