from django.urls import re_path

from .consumers import ChatConsumer, GameConsumer

ws_urlpatterns = [
    re_path(r"ws/game/(?P<game_id>\w+)/$", GameConsumer.as_asgi()),
    re_path(
        r"ws/chat/(?P<game_code>\w+)/(?P<username>\w+)/$",
        ChatConsumer.as_asgi(),
    ),
]
