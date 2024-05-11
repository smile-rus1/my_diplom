from notifications.models import NotificationsDays
from services.dto.notifications.notifications_days_entity import NotificationsDaysEntity

from services.notifications.baseDAO import BaseDAO


class NotificationsDaysDAO(BaseDAO):
    def _orm_to_entity(self, notifications_days_orm: NotificationsDays):
        return NotificationsDaysEntity(
            pk=notifications_days_orm.pk,
            days=notifications_days_orm.days
        )

    def fetch_all(self) -> list[NotificationsDaysEntity]:
        return list(map(self._orm_to_entity, NotificationsDays.objects.all().order_by("id")))
