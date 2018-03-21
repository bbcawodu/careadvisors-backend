from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOSTURL = "https://metricsbackend-demo.herokuapp.com"

if DEBUG:
    CORS_ORIGIN_WHITELIST += ('localhost:8080', 'localhost:5000')

CORS_ORIGIN_ALLOW_ALL = True
