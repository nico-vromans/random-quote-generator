"""
WSGI config for rqg project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='rqg.settings')
os.environ.setdefault(key='DJANGO_CONFIGURATION', value='Default')

application = get_wsgi_application()
