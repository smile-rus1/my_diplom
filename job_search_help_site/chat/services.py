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
        user=data_application.get("user"),
        room=data_application.get("room"),
        content=data_application.get("content"),
        first_name=data_application.get("first_name"),
        last_name=data_application.get("last_name"),
    )


def exit_from_room_chat(user, room_id: int) -> None:
    """
    Выход из комнаты чата пользователю.
    """
    try:
        room = get_room_by_id(user, room_id)
        room.allowed_users.remove(user)

        _check_exists_users_in_room(room)

    except AttributeError:
        return


def _check_exists_users_in_room(room: models.Room):
    """
    Проверяет существуют ли еще пользователи в комнате.
    """
    if room.allowed_users.count() == 0:
        room.application.delete()
        room.delete()
