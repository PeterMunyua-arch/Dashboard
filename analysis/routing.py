from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from .consumers import UpdateConsumer
import analysis.routing

application = ProtocolTypeRouter({
    "websocket": URLRouter(
        path("ws/updates/", UpdateConsumer.as_asgi()),
        analysis.routing.application
    ),
})