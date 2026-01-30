"""
ASGI config for secureHome project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secureHome.settings')
from django.core.asgi import get_asgi_application
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import Secur.routing 




application = ProtocolTypeRouter({
    "http" :  django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            Secur.routing.websocket_urlpatterns
        ) 
    ) 
})
