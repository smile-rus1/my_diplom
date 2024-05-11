import datetime
from dataclasses import dataclass


@dataclass
class NotificationsTimeEntity:
    pk: int
    start_time_send: datetime.datetime
    end_start_send: datetime.datetime
