"""
Defines settings for running the project locally on a Heroku installation
"""

from picbackend.settings.base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

HOSTURL = "http://localhost:5000"