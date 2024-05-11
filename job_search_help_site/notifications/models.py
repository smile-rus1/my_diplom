from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()

"""
Видел что некоторые пишут логику прямо в модльках мб попробывать!
"""


class TypeNotifications(models.Model):
    """
    Models which representations a few type of notifications such as:
    telegram/email and etc...
    """
    TELEGRAM = "telegram"
    EMAIL = "email"
    PHONE = "phone"

    CHOICES = [
        (TELEGRAM, 'Telegram'),
        (EMAIL, 'Email'),
        (PHONE, 'Phone'),
    ]

    type_notification = models.CharField(null=False, max_length=20, choices=CHOICES)

    def __str__(self):
        return f"{self.type_notification}"

    class Meta:
        verbose_name_plural = "Типы уведомления пользователей"


class NotificationsTime(models.Model):
    """
    Models for time send notifications to users.
    """
    start_time_send = models.TimeField()
    end_start_send = models.TimeField()

    @staticmethod
    def get_default():
        from django.db import connection
        from django.db.migrations.executor import MigrationExecutor

        if MigrationExecutor(connection).loader.graph.leaf_nodes():
            return None
        else:
            random_notification_time = NotificationsTime.objects.order_by('?').first()
            if random_notification_time:
                return random_notification_time.id
            else:
                return None

    def __str__(self):
        return f"{self.start_time_send.strftime('%I:%M %p')} - {self.end_start_send.strftime('%I:%M %p')}"

    class Meta:
        verbose_name_plural = "Время уведомления пользователя"


class NotificationsDays(models.Model):
    """
    Models for notifications users on days.
    """
    DAYS_CHOICES = [
        ("MONDAY", _("Monday (Понедельник)")),
        ("TUESDAY", _("Tuesday (Вторник)")),
        ("WEDNESDAY", _("Wednesday (Среда)")),
        ("THURSDAY", _("Thursday (Четверг)")),
        ("FRIDAY", _("Friday (Пятница)")),
        ("SATURDAY", _("Saturday (Суббота)")),
        ("SUNDAY", _("Sunday (Воскресенье)")),
    ]

    days = models.CharField(
        max_length=15,
        unique=True,
        null=False,
        default="Monday",
        choices=DAYS_CHOICES
    )

    def __str__(self):
        return f"{self.days}"

    class Meta:
        verbose_name_plural = "Дни уведомления пользователя"


class Notifications(models.Model):
    """
    Models for users which subscribers to notifications.
    """
    ROLE_APPLICANT = 'applicant'
    ROLE_EMPLOYER = 'company'

    ROLE_CHOICES = [
        (ROLE_APPLICANT, 'Applicant'),
        (ROLE_EMPLOYER, 'Employer'),
    ]

    user = models.ManyToManyField(User)
    type_notifications = models.ManyToManyField(TypeNotifications, verbose_name="Тип уведомления")
    time_notifications = models.ForeignKey(
        NotificationsTime,
        on_delete=models.SET_DEFAULT,
        default=NotificationsTime.get_default
    )
    days_notifications = models.ManyToManyField(NotificationsDays)
    is_subscribe = models.BooleanField(default=True, verbose_name="Подписан на рассылку", null=False)
    date_subscribe = models.DateTimeField(auto_now=True, verbose_name="Время подписки на рассылку уведомления")
    notification_recipient = models.CharField(null=False, max_length=20, verbose_name="Место отправления получателю")
    role = models.CharField(null=False, max_length=20, choices=ROLE_CHOICES, verbose_name="Роль пользователя")

    class Meta:
        verbose_name_plural = "Подписка на уведомления"
        ordering = ["-date_subscribe"]


class NotificationsApplicant(models.Model):
    """
    Models for notifications users, which have role applicant.
    """
    notifications = models.ForeignKey(Notifications, on_delete=models.CASCADE)
    resume = models.ForeignKey("search_site.Resume", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Уведомления кандидатам"
        ordering = ["-resume__updated_at"]
        unique_together = ('notifications', 'resume')


class NotificationsEmployer(models.Model):
    """
    Models for notifications users, which have role employer.
    """
    notifications = models.ForeignKey(Notifications, on_delete=models.CASCADE)
    vacancy = models.ForeignKey("search_site.Vacancy", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Уведомления компаниям"
        ordering = ["-vacancy__updated_at"]
        unique_together = ('notifications', 'vacancy')
