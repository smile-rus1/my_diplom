from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from . import models
from services.notifications import *
from tools import sessions, UsersTools


class BaseView(View):
    """
    Base view for any views.
    """
    model = models.Notifications.objects.all()


class SubscribeNotificationsView(BaseView):
    """
    View for subscribe on notifications in app.
    """
    template_name = "notifications/main_notifications_page.html"

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        session_template = request.session.get("template")

        if session_template is None:
            session_template = sessions.SessionsForGetTemplate.set_template_in_session(request)

        context = {
            "template": session_template,
            "days": notificationsdaysDAO.NotificationsDaysDAO().fetch_all(),
            "time": notificationstimeDAO.NotificationsTimeDAO().fetch_all(),
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        if request.POST.get("type_notifications") == "email":
            notification_recipient = request.user.email
        elif request.POST.get("type_notifications") == "telegram":
            notification_recipient = request.POST.get("notification_recipient")

        notifications_entity = notificationsDAO.NotificationsEntityCreate(
                user=request.user,
                time_notifications=request.POST.get("time"),
                type_notifications=request.POST.get("type_notifications"),
                days_notifications=request.POST.getlist("days"),
                notification_recipient=notification_recipient,
                role=UsersTools.check_user_role(request.user)
            )

        notifications = notificationsDAO.NotificationsDAO().create_model(notifications_entity)

        if notifications is None:
            messages.error(request, "Произошла обшибка, попробуйте чуть позже!")
            return redirect("notifications:notifications")

        messages.success(request, "Подписка на уведомление оформлена!")
        return redirect("notifications:subscribe_notifications")


class AllUserSubscribesOnNotificationsView(BaseView):
    """
    View for viewing signed notifications.
    """
    template_name = "notifications/all_user_subscribes.html"
    model = models.Notifications.objects.prefetch_related(
        'user',
        'days_notifications',
        'notificationsapplicant_set__notifications',
        'notificationsemployer_set__notifications',
    ).all()

    def get(self, request, *args, **kwargs):
        session_template = request.session.get("template")

        if session_template is None:
            session_template = sessions.SessionsForGetTemplate.set_template_in_session(request)

        context = {
            "template": session_template,
            "all_subscribes": self.model.filter(user=request.user)
        }

        return render(request, self.template_name, context=context)


class SubscribeUserOnNotificationView(BaseView):
    """
    Subscribe of user on notification.
    """
    template_name = "notifications/all_user_subscribes.html"

    def post(self, request, *args, **kwargs):
        lst_ids = request.POST.getlist('subscribe_ids[]')

        if not notificationsDAO.NotificationsDAO().subscribe_notification(lst_ids):
            messages.success(request, "Произошла ошибка")
            return JsonResponse({'success': False})

        messages.success(request, "Вы подписались на уведомления!")
        return JsonResponse({'success': True})


class UnsubscribeUserOnNotificationView(BaseView):
    """
    Unsubscribe of user on notification.
    """
    template_name = "notifications/all_user_subscribes.html"

    def post(self, request, *args, **kwargs):
        lst_ids = request.POST.getlist('subscribe_ids[]')
        if not notificationsDAO.NotificationsDAO().unsubscribe_notification(lst_ids):
            messages.success(request, "Произошла ошибка")
            return JsonResponse({'success': False})

        messages.success(request, "Вы отписались от уведомлений!")
        return JsonResponse({'success': True})


class DeleteSubscribeUserNotificationsView(BaseView):
    template_name = "notifications/all_user_subscribes.html"

    def post(self, request, *args, **kwargs):
        lst_ids = request.POST.getlist('subscribe_ids[]')
        if not notificationsDAO.NotificationsDAO().delete_notifications(lst_ids):
            messages.success(request, "Произошла ошибка")
            return JsonResponse({'success': False})

        messages.success(request, "Вы удалили подписку!")
        return JsonResponse({'success': True})
