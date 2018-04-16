from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOSTURL = "https://picbackend-dev.herokuapp.com"

if DEBUG:
    SECURE_SSL_REDIRECT = False

    CORS_ORIGIN_WHITELIST += ('localhost:8080/', 'localhost:5000/', 'localhost:3000/')
    CSRF_TRUSTED_ORIGINS += ('localhost:8080/', 'localhost:5000/', 'localhost:3000/')

CORS_ORIGIN_ALLOW_ALL = True
