"""
ASGI config for ong_platform project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ong_platform.settings')

application = get_asgi_application()
