from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from . import services


@login_required
def index(request):
    rooms = services.get_all_room(request)

    return render(
        request,
        "chat/index.html",
        {
            "rooms": rooms
        }
    )


@login_required
def room(request, room_id: int):
    room_ = services.get_room_by_id(request.user, room_id)
    if room_ is None:
        return redirect("index_chat")

    messages = services.get_messages(room_)

    return render(
        request,
        "chat/room.html",
        {
            "room": room_,
            "messages": messages,
        }
    )


def exit_from_room_chat(request, room_id: int):
    """
    Выход из комнаты чата.
    """
    services.exit_from_room_chat(request.user, room_id)
    return redirect("index_chat")
