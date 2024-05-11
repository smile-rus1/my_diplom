from dataclasses import dataclass
from notifications.models import (
    User,
    TypeNotifications,
    NotificationsTime,
    NotificationsDays,
)


@dataclass
class NotificationsEntity:
    pk: int
    user: User
    type_notifications: TypeNotifications
    time_notifications: NotificationsTime
    days_notifications: NotificationsDays
    notification_recipient: str
    role: str


@dataclass
class NotificationsEntityCreate:
    user: User
    type_notifications: str
    time_notifications: int
    days_notifications: list[int]
    notification_recipient: str
    role: str
