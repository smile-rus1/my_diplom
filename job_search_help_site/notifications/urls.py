from django.urls import path
from . import views


app_name = 'notifications'

urlpatterns = [
    path("", views.SubscribeNotificationsView.as_view(), name="subscribe_notifications"),
    path("all_subscribes", views.AllUserSubscribesOnNotificationsView.as_view(), name="all_user_subscribes"),
    path("subscribe/", views.SubscribeUserOnNotificationView.as_view(), name="subscribe_notification"),
    path("unsubscribe/", views.UnsubscribeUserOnNotificationView.as_view(), name="unsubscribe_notification"),
    path("delete_subscribe/", views.DeleteSubscribeUserNotificationsView.as_view(), name="delete_notification"),
]
