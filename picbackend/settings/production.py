from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

HOSTURL = "https://picbackend.herokuapp.com"

if not DEBUG:
    CORS_ORIGIN_WHITELIST += ('localhost:8080', 'localhost:5000', 'localhost:3000', '192.168.1.92', '192.168.1.8080',
                              'localhost:8080/', 'localhost:5000/', 'localhost:3000/', '192.168.1.92/', '192.168.1.8080/')
    CSRF_TRUSTED_ORIGINS += ('localhost:8080', 'localhost:5000', 'localhost:3000', '192.168.1.92', '192.168.1.8080',
                             'localhost:8080/', 'localhost:5000/', 'localhost:3000/', '192.168.1.92/', '192.168.1.8080/')
