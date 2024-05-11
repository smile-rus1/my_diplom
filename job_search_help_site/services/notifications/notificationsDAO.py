from django.db import transaction

from search_site.models import Resume, Vacancy
from services.dto.notifications.notifications_entity import NotificationsEntity, NotificationsEntityCreate
from services.notifications.baseDAO import BaseDAO

from notifications.models import (
    Notifications,
    TypeNotifications,
    NotificationsTime,
    NotificationsDays,
    NotificationsApplicant,
    NotificationsEmployer
)


class NotificationsDAO(BaseDAO):
    def _orm_to_entity(self, notifications_orm: Notifications):
        return NotificationsEntity(
            pk=notifications_orm.pk,
            user=notifications_orm.user,
            type_notifications=notifications_orm.type_notifications,
            time_notifications=notifications_orm.time_notifications,
            days_notifications=notifications_orm.days_notifications,
            notification_recipient=notifications_orm.notification_recipient,
            role=notifications_orm.role
        )

    def fetch_all(self) -> list[NotificationsEntity]:
        return Notifications.objects.prefetch_related(
            'user',
            'type_notifications',
            'days_notifications'
        ).all()

    def get_random_model(self, model, **filters):
        return model.objects.filter(**filters).order_by("?").first()

    def create_model(self, entity: NotificationsEntityCreate) -> Notifications | None:
        try:
            with transaction.atomic():
                type_notifications = self.fetch_one_from_model(
                    TypeNotifications, type_notification=entity.type_notifications
                )
                time_notifications = self.fetch_one_from_model(
                    NotificationsTime, id=entity.time_notifications
                )
                days_notifications = NotificationsDays.objects.filter(pk__in=entity.days_notifications)
                notification = Notifications.objects.create(
                    time_notifications=time_notifications,
                    notification_recipient=entity.notification_recipient,
                    role=entity.role,
                )
                notification.type_notifications.add(type_notifications)
                notification.days_notifications.add(*days_notifications)
                notification.user.add(entity.user)

                if entity.role == "applicant":
                    NotificationsApplicant.objects.create(
                        notifications=notification,
                        resume=self.get_random_model(Resume, applicant=entity.user.applicant)
                    )

                elif entity.role == "company":
                    NotificationsEmployer.objects.create(
                        notifications=notification,
                        vacancy=self.get_random_model(Vacancy, company=entity.user.company)
                    )
                return notification
        except:
            return

    def unsubscribe_notification(self, lst_ids: list[int]) -> bool:
        try:
            with transaction.atomic():
                for sub_id in lst_ids:
                    notification = self.fetch_one_from_model(Notifications, id=sub_id)
                    notification.is_subscribe = False
                    notification.save()
                return True
        except:
            return False

    def subscribe_notification(self, lst_ids: list[int]) -> bool:
        try:
            with transaction.atomic():
                for sub_id in lst_ids:
                    notification = self.fetch_one_from_model(Notifications, id=sub_id)
                    notification.is_subscribe = True
                    notification.save()
                return True
        except:
            return False

    def delete_notifications(self, lst_ids: list[int]) -> bool:
        try:
            with transaction.atomic():
                for sub_id in lst_ids:
                    notification = self.fetch_one_from_model(Notifications, id=sub_id)
                    notification.delete()
                return True
        except:
            return False
