from . import models

from django.contrib.auth import get_user_model

User = get_user_model()


def get_all_room(request) -> models.Room:
    if hasattr(request.user, 'applicant'):
        return models.Room.objects.filter(application__applicant__user=request.user).all()

    if hasattr(request.user, 'company'):
        return models.Room.objects.filter(application__vacancy__company__user=request.user).all()


def get_room_by_id(user, room_id: int) -> models.Room | None:
    """
    Возвращает комнату по id.
    """
    try:
        room = models.Room.objects.get(id=room_id)
        if user in room.allowed_users.all():
            return room
        else:
            return None

    except models.Room.DoesNotExist:
        return None


def get_messages(room: models.Room) -> models.Message:
    """
    Возвращает messages, по room.
    """
    return models.Message.objects.filter(room=room)[0:25]


def create_message_for_cover_letter_of_candidate(**data_application) -> None:
    """
    Создает первое сообщение в модель Message, как сопроводительное письмо.
    """
    models.Message.objects.create(
        user=data_application["user"],
        room=data_application["room"],
        content=data_application["content"],
        first_name=data_application["first_name"],
        last_name=data_application["last_name"],
    )
