import random

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from managers import models as managers_model
from . import models


@receiver(post_save, sender=models.Application)
def set_is_invited(sender, instance, created, **kwargs):
    if created and instance.cover_letter == "":
        instance.is_invited = True
        instance.save()


@receiver(post_save, sender=models.RequestToVerificationUser)
def create_verification_user_role(sender, instance, created, **kwargs):
    if created:
        try:
            with transaction.atomic():
                all_managers = models.CustomUser.objects.filter(is_staff=True, is_superuser=False)
                random_manager = random.choice(all_managers)

                managers_model.VerificationUserRole.objects.create(
                    request_verification=instance,
                    manager=random_manager
                )

        except Exception as e:
            print(f"Exception in create model: {e}")


post_save.connect(create_verification_user_role, sender=models.RequestToVerificationUser)
