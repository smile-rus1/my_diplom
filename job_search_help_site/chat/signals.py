# chat/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Room
from . import services
from search_site.models import Application


@receiver(post_save, sender=Application)
def create_chat_room(sender, instance, created, **kwargs):
    if created:
        room_id = instance.id

        candidate = instance.applicant
        company = instance.vacancy.company.user

        name_company = instance.company
        name_resume = instance.resume.name_of_resume

        new_room = Room.objects.create(
            name_company=name_company,
            name_resume=name_resume,
            application=instance
        )

        new_room.allowed_users.add(candidate.user, company)

        # Отправляем сигнал через WebSocket о создании комнаты чата
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room_id}",  # Используем room_id для названия группы комнаты
            {
                'type': 'chat.created',
                'message': 'Room created successfully',
                'room_id': new_room.id,
            }
        )

        if instance.is_invited:
            services.create_message_for_cover_letter_of_candidate(
                user=candidate.user,
                room=new_room,
                content=""
            )

        elif instance.cover_letter != "":
            services.create_message_for_cover_letter_of_candidate(
                user=candidate.user,
                room=new_room,
                content=instance.cover_letter,
                first_name=candidate.first_name,
                last_name=candidate.second_name,
            )

