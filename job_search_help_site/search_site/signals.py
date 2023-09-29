from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application


@receiver(post_save, sender=Application)
def set_is_invited(sender, instance, created, **kwargs):
    if created:
        instance.is_invited = True
        instance.save()
