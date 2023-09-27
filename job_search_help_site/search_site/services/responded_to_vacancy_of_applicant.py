from django.http import Http404

from search_site import models


def get_all_responded_to_vacancy(user: models.CustomUser) -> models.Application:
    """
    Возвращает всех кандидатов, которые откликнулись на вакансии.
    """
    return models.Application.objects \
        .filter(applicant__isnull=False).select_related("applicant__user", "vacancy__company") \
        .filter(vacancy__company=user.company)


def show_all_info_about_applicant_of_application(
        user: models.CustomUser,
        applicant_id: int,
        vacancy_id: int
) -> models.Application:
    """
    Показывает всю инфомацию о applicant, которые откликнулись на вакансию.
    """
    try:
        return models.Application.objects \
            .filter(applicant__isnull=False)\
            .select_related("applicant__user", "vacancy__company") \
            .filter(vacancy__company=user.company, applicant=applicant_id, vacancy=vacancy_id).first()

    except:
        raise Http404("Не найдено")


def show_all_info_about_applicant(resume_id: int) -> models.Application:
    """
    Показывает всю информацию о кандидате по переданному
    """
    return models.Application.objects.filter(applicant__isnull=False).select_related("applicant__user")\
        .filter(resume=resume_id).first()


def change_application_status_of_applicant(**user_data: [int, str]) -> models.Application:
    """
    Меняет status у applicant по id вакансии.
    """
    return models.Application.objects.filter(id=user_data.get("application_id"))\
        .update(status=user_data.get("status"))

