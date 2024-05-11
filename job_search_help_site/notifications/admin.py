from django.contrib import admin
from .models import TypeNotifications, NotificationsDays, NotificationsTime, Notifications, NotificationsEmployer, NotificationsApplicant


class CustomTypeNotificationsAdmin(admin.ModelAdmin):
    list_display = ("id", 'type_notification',)
    ordering = ['id']


class CustomNotificationsAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_notifications",
        "get_type_notifications",
        "notification_recipient",
        "get_time_notifications",
        "get_days_notifications",
        "date_subscribe",
        "role",
        "is_subscribe"
    )
    ordering = ["date_subscribe", "is_subscribe"]

    def get_time_notifications(self, obj):
        return f"{obj.time_notifications.start_time_send} - {obj.time_notifications.end_start_send}"

    def get_type_notifications(self, obj):
        return ', '.join([type_notification.type_notification for type_notification in obj.type_notifications.all()])

    def get_user_notifications(self, obj):
        return ', '.join([user.email for user in obj.user.all()])

    def get_days_notifications(self, obj):
        return ', '.join([day.days for day in obj.days_notifications.all()])

    get_time_notifications.short_description = "Время уведомления"
    get_type_notifications.short_description = "Тип уведомления"
    get_user_notifications.short_description = "Пользователь"
    get_days_notifications.short_description = "Дни получения"


class CustomNotificationsApplicantAdmin(admin.ModelAdmin):
    ...


class CustomNotificationsEmployerAdmin(admin.ModelAdmin):
    ...


class CustomNotificationTimeAdmin(admin.ModelAdmin):
    list_display = ("start_time_send", "end_start_send")
    ordering = ["id"]


class CustomNotificationDaysAdmin(admin.ModelAdmin):
    list_display = ("days", )
    ordering = ["id"]


admin.site.register(TypeNotifications, CustomTypeNotificationsAdmin)
admin.site.register(Notifications, CustomNotificationsAdmin)
admin.site.register(NotificationsApplicant, CustomNotificationsApplicantAdmin)
admin.site.register(NotificationsEmployer, CustomNotificationsEmployerAdmin)
admin.site.register(NotificationsTime, CustomNotificationTimeAdmin)
admin.site.register(NotificationsDays, CustomNotificationDaysAdmin)


