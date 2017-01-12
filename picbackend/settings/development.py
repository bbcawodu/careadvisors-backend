"""
Defines settings for running the project on our development host url via a Heroku installation
"""

from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

HOSTURL = "https://picbackend-dev.herokuapp.com"