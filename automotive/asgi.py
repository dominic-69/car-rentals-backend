import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import apps.chat.routing

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'automotive.settings')

# Initialize Django ASGI application
django_asgi_app = get_asgi_application()

# Main ASGI application
application = ProtocolTypeRouter({

    # Handle standard HTTP requests
    "http": django_asgi_app,

    # Handle WebSocket connections with authentication
    "websocket": AuthMiddlewareStack(
        URLRouter(
            apps.chat.routing.websocket_urlpatterns
        )
    ),
})