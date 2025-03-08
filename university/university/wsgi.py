"""
WSGI config for university project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
import os
import sys

path = '/home/sc22mibs/django/university'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'university.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()