"""
Defines settings for running the project on our development host url via a Heroku installation
"""

from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

HOSTURL = "https://picbackend-dev.herokuapp.com"

if DEBUG:
    CORS_ORIGIN_WHITELIST += ('localhost:8080', 'localhost:5000')

CORS_ORIGIN_ALLOW_ALL = True
