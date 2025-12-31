"""
WSGI config for ong_platform project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ong_platform.settings')

application = get_wsgi_application()
