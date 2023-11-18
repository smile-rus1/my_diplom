import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Room, Message, User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f"chat_{self.room_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Get room
        room = await self.get_room()
        sender = self.scope['user']

        user = await self.get_user_by_email(sender)
        user_data = await self.prepare_user_data(user)

        # save in db message
        await self.save_message(
            sender,
            room,
            message,
            last_name=user_data[0],
            first_name=user_data[1],
        )

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'sender': sender.email,
                "last_name": user_data[0],
                "first_name": user_data[1]
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        # prepare data user
        user = await self.get_user_by_email(sender)
        user_data = await self.prepare_user_data(user)

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            "sender": sender,
            "last_name": user_data[0],
            "first_name": user_data[1]
        }))

    async def get_room(self):
        return await self.get_object_or_404(Room, id=self.room_id)

    @sync_to_async
    def get_object_or_404(self, model, **kwargs):
        obj = model.objects.filter(**kwargs).first()
        if not obj:
            raise Exception(f"{model.__name__} not found")
        return obj

    @sync_to_async
    def save_message(self, email, room, message, **data_user):
        user = User.objects.get(email=email)
        room = Room.objects.get(id=room.id)

        Message.objects.create(
            user=user,
            room=room,
            content=message,
            first_name=data_user["first_name"],
            last_name=data_user["last_name"],
        )

    @sync_to_async
    def get_user_by_email(self, email: str) -> User:
        """
        Возвращает пользователя по email.
        """
        user = User.objects.filter(email=email).first()
        return user

    @sync_to_async
    def prepare_user_data(self, user: User):
        try:
            return user.company.second_name_user, user.company.name_user
        except:
            return user.applicant.second_name, user.applicant.first_name
