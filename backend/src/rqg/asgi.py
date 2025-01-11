"""
ASGI config for rqg project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from configurations.asgi import get_asgi_application

os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='rqg.settings')
os.environ.setdefault(key='DJANGO_CONFIGURATION', value='Default')

application = get_asgi_application()
