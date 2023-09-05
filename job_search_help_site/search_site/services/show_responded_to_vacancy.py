from search_site import models


def get_all_responded_to_vacancy(user: models.CustomUser) -> models.Applicant:
    """
    Возвращает всех кандидатов, которые откликнулись на вакансии.
    """
    applications_for_company = models.Application.objects\
        .filter(applicant__isnull=False).select_related("applicant__user", "vacancy__company")\
        .filter(vacancy__company=user.company)
    return applications_for_company

