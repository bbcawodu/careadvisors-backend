from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOSTURL = "https://metricsbackend-demo.herokuapp.com"

if DEBUG:
    CORS_ORIGIN_WHITELIST += ('localhost:8080', 'localhost:5000', 'localhost:3000')
    CSRF_TRUSTED_ORIGINS += ('localhost:8080', 'localhost:5000', 'localhost:3000')
