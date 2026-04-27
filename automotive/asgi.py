import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

import apps.chat.routing

# 🔥 SET SETTINGS
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automotive.settings')

# 🔥 INIT DJANGO FIRST
django_asgi_app = get_asgi_application()

# 🔥 MAIN APPLICATION
application = ProtocolTypeRouter({

    # HTTP requests
    "http": django_asgi_app,

    # WebSocket requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})