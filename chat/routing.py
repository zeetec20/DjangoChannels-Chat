from django.urls import path

from .consumer import Online, Chat

websocket_urlpatterns = [
    path('ws/user/online/', Online),
    path('ws/user/chat/<user>', Chat)
]