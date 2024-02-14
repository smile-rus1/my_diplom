from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class VerificationUserRole(models.Model):
    """
    Model for verification company on authenticity.
    """
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": True}
    )
    request_verification = models.ForeignKey(
        "search_site.RequestToVerificationUser",
        on_delete=models.CASCADE
    )
    date_confirm = models.DateTimeField(
        null=True,
        default=None,
        verbose_name="Date of confirm request"
    )
    confirm = models.BooleanField(
        default=False,
        verbose_name="Confirm of request"
    )

    class Meta:
        ordering = ["-date_confirm"]
        verbose_name_plural = "Потверждение верификации роли пользователя"
