import os
from django.core.asgi import get_asgi_application
from .routing import application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'analysis.settings')
application = get_asgi_application()