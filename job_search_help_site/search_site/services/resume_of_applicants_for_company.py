from django.shortcuts import get_object_or_404

from search_site import models

from . import algorithm_search_resume_of_applicants_for_company


def get_resume_for_company_by_algorithm_in_main_page(user: models.CustomUser):
    """
    Возвращает кандидатов на главную страницу компаний.
    """
    vacancy = models.Vacancy.objects.\
        filter(company=get_object_or_404(models.Company, user=user), is_published=True)\
        .order_by("?").first()

    if vacancy is None:
        return models.Resume.objects.filter(is_published=True).order_by("?")[:6]
    return models.Resume.objects.filter(algorithm_search_resume_of_applicants_for_company
                                        .get_all_desired_resume_of_applicants(vacancy))[:6]
