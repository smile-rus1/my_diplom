from django.db.models import Q

from search_site import models

from ._algorithms_of_search import search_vacancy


def get_all_vacancy_by_criterion(criteria: str) -> models.Vacancy:
    """
    Возвращает все Vacancy, в которых находятся эти критерии, которые
    были переданы.
    """
    if criteria == "ALL_VACANCY":
        return search_vacancy.get_all_model()
    return models.Vacancy.objects.filter(_get_vacancy_by_criteria(criteria), is_published=True)\
        .prefetch_related("company")\
        .order_by("-updated_at", "-created_at")


def _get_vacancy_by_criteria(criteria: str) -> Q:
    """
    Возвращает все вакансии, у которых есть совпадения по критериям.
    """
    q = Q()
    for cr in criteria.split():
        q |= Q(key_skills__icontains=cr.strip()) | Q(company__title_company__icontains=cr.strip()) \
             | Q(specialization__icontains=cr.strip()) | Q(title_vacancy__icontains=cr.strip())
    return q


def get_vacancies_by_parameters(request) -> models.Vacancy:
    """
    Возвращает вакансии, по параметрам переданным в
    URL заголовках/параметров.
    """
    combined_vacancies = None

    if request.GET.get("time_employment"):
        query = search_vacancy.get_vacancies_by_time_employment(request.GET.get("time_employment"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("specialization"):
        query = search_vacancy.get_vacancies_by_specialization(request.GET.get("specialization"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("experience"):
        query = search_vacancy.get_vacancies_by_experience(request.GET.get("experience"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("date_publication"):
        query = search_vacancy.get_vacancies_by_publication_time(request.GET.get("date_publication"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if combined_vacancies is None:
        return ""
    return combined_vacancies
