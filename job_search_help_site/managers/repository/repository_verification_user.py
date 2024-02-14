from distutils.util import strtobool

from django.db.models import Case, When, Value, CharField, F

from .base_repository import BaseRepository


class RepositoryVerificationUserRole(BaseRepository):
    """
    Repository of model VerificationUserRole.
    """
    def get_verification_user_roles_for_manager(self, manager, filters: dict):
        """
        Get all records users, which need to verify role by manager.
        """
        try:
            if filters:
                filters["manager"] = manager
                filter_queryset = self.get_verification_user_roles_for_manager_by_filters(filters)
                return filter_queryset

            verification_user_role_queryset = self.model.objects.annotate(
                phone_number=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then='request_verification__user__applicant__phone'),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__phone_company'),
                    default=Value(''),
                    output_field=CharField(),
                ),
                first_name=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then="request_verification__user__applicant__first_name"),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__name_user'),
                    default=Value(''),
                    output_field=CharField()
                ),
                second_name=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then="request_verification__user__applicant__second_name"),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__second_name_user'),
                    default=Value(''),
                    output_field=CharField()
                )
            )
            return verification_user_role_queryset.filter(manager=manager).all()

        except Exception as e:
            print(f"EXEPTION {e}")

        return None

    def get_verification_user_role_by_id(self, verification_user_id: int, manager):
        return self.get_by_criteria(id=verification_user_id, manager=manager)

    def get_verification_user_roles_for_manager_by_filters(self, filters: dict):
        """
        Get all records users by PATH param.
        """
        try:
            is_confirm = filters.get("is_confirm")
            is_confirm_bool = bool(strtobool(is_confirm)) if is_confirm is not None else None
            if is_confirm_bool is not None:
                filters["is_confirm"] = is_confirm_bool
            filter_queryset = self.model.objects.annotate(
                phone_number=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then='request_verification__user__applicant__phone'),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__phone_company'),
                    default=Value(''),
                    output_field=CharField(),
                ),
                first_name=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then="request_verification__user__applicant__first_name"),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__name_user'),
                    default=Value(''),
                    output_field=CharField()
                ),
                second_name=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then="request_verification__user__applicant__second_name"),
                    When(request_verification__user__company__isnull=False,
                         then='request_verification__user__company__second_name_user'),
                    default=Value(''),
                    output_field=CharField()
                ),
                role=Case(
                    When(request_verification__user__applicant__isnull=False,
                         then=Value("applicant")),
                    When(request_verification__user__company__isnull=False,
                         then=Value("company")),
                    default=Value(''),
                    output_field=CharField()
                ),
                is_confirm=F("confirm")
            )

            return filter_queryset.filter(**filters).all()
        except Exception as e:
            print(f"EXEPTION IN filtr {e}")
        return None
