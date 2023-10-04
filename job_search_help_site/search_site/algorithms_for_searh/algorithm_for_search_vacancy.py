from django.db.models import Q

from search_site import models


def get_all_vacancy_by_criterion(criteria: str) -> models.Vacancy:
    """
    Возвращает все Vacancy, в которых находятся эти критерии, которые
    были переданы.
    """
    if criteria == "ALL_VACANCY":
        return _get_all_vacancy()
    return models.Vacancy.objects.filter(_get_vacancy_by_criteria(criteria), is_published=True)\
        .prefetch_related("company")\
        .order_by("-publication_time", "-created_at")


def _get_vacancy_by_criteria(criteria: str) -> Q:
    """
    Возвращает все вакансии, у которых есть совпадения по критериям.
    """
    q = Q()
    for cr in criteria.split():
        q |= Q(key_skills__icontains=cr.strip()) | Q(company__title_company__icontains=cr.strip()) \
             | Q(specialization__icontains=cr.strip()) | Q(title_vacancy__icontains=cr.strip())
    return q


def _get_all_vacancy() -> models.Vacancy:
    """
    Возвращает все вакансии для страницы applicant/search/
    """
    return models.Vacancy.objects.all()
