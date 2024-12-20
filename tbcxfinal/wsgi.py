"""
WSGI config for tbcxfinal project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import atexit
from django.core.cache import cache
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tbcxfinal.settings')

application = get_wsgi_application()


def delete_cache_on_exit():
    cache_key = "popular_locations"
    deleted = cache.delete(cache_key)
    print(f"Cache key '{cache_key}' deleted on exit: {deleted}")


atexit.register(delete_cache_on_exit)
