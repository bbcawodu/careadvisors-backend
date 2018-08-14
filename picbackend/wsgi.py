"""
WSGI config for picproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "picbackend.settings.demo")
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "picbackend.settings.production")
>>>>>>> dev-db

application = get_wsgi_application()

"""
This section of code serves static files in production
"""

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
