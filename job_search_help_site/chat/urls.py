from django.urls import path
# from . import consumers
from . import views


urlpatterns = [
    path("main/", views.index, name="index_chat"),
    path("room/<int:room_id>", views.room, name="room"),
    path("exit_from_room_chat/<int:room_id>", views.exit_from_room_chat, name="exit_from_room_chat")
    # path("")
    # path('ws/chat/<application_id>/', consumers.ChatConsumer.as_asgi(), name='chat'),
]
