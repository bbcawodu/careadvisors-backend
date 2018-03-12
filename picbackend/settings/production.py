from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

HOSTURL = "https://picbackend.herokuapp.com"

if DEBUG:
    CORS_ORIGIN_WHITELIST += ('localhost:8080',)
