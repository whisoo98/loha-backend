from django.conf.urls import url
from . import consumers

ASGI_APPLICATION = "loha.routing.application"

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]
