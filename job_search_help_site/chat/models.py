from django.db import models
from django.contrib.auth import get_user_model

from search_site import models as models_site


User = get_user_model()


class Room(models.Model):
    name_company = models.CharField(max_length=255)
    name_resume = models.CharField(max_length=255)
    application = models.ForeignKey(models_site.Application, on_delete=models.CASCADE)
    allowed_users = models.ManyToManyField(User, related_name='allowed_rooms', blank=True)


class Message(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_added',)
