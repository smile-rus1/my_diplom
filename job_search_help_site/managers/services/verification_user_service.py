from django.utils import timezone
from django.db import transaction

from .. import tasks


class VerificationUserService:
    @staticmethod
    def confirm_user_role(model, data) -> bool | None:
        """
        Confirm user role.
        """
        with transaction.atomic():
            try:
                model.date_confirm = timezone.now()
                model.confirm = data.get("confirm")
                model.request_verification.user.applicant.is_confirmed = data.get("confirm")
                model.request_verification.user.applicant.save()
                model.save()

                data_notifications = {
                    "subject": "Потверждение на сайте",
                    "message": f"{VerificationUserService._get_message_is_user_verified(data.get('confirm'))}",
                    "email_recipient": model.request_verification.user.email
                }

                tasks.send_notifications_email.delay(data_notifications)

                return True
            except Exception as e:
                print(f"Exeption {e}")

    @staticmethod
    def _get_message_is_user_verified(is_confirmed: bool) -> str:
        if is_confirmed:
            return "Ваша заявка на подтверждение на нашем сайте успешно завершена. Теперь вам доступны некоторые " \
                   "закрытые функции."
        return "К сожалению, ваша заявка на подтверждение займет больше времени для рассмотрения. " \
               "Если возникнет срочное потверждение, обратитесь в техподдержку."
