from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from base import routing as chat_routing

application= ProtocolTypeRouter({
    "websocket": URLRouter(
        chat_routing.websocket_urlpatterns
    )
})