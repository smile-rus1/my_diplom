from notifications.models import NotificationsTime
from services.dto.notifications.notifications_time_entity import NotificationsTimeEntity

from services.notifications.baseDAO import BaseDAO


class NotificationsTimeDAO(BaseDAO):
    def _orm_to_entity(self, notifications_time_orm: NotificationsTime):
        return NotificationsTimeEntity(
            pk=notifications_time_orm.pk,
            start_time_send=notifications_time_orm.start_time_send,
            end_start_send=notifications_time_orm.end_start_send
        )

    def fetch_all(self) -> list[NotificationsTimeEntity]:
        return list(map(self._orm_to_entity, NotificationsTime.objects.all().order_by("id")))
