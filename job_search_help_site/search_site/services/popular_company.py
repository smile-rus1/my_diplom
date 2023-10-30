from django.db.models import Count
from django.core.cache import cache

from search_site import models


def get_most_popular_company_on_total_vacancy() -> models.Company:
    """
    Возвращает популярные компании по кол-ву вакансий.
    """
    popular_company = cache.get("popular_company")

    if popular_company is None:
        popular_company = models.Company.objects.annotate(vacancy_count=Count("vacancy")).order_by('-vacancy_count')
        cache.set("popular_company", popular_company, 300)
    return popular_company


def get_lst_company_data(popular_company: models.Company) -> list[models.Company]:
    lst_company: list[dict] = []
    for company in popular_company:
        lst_company.append({"company": company, "vacancy_count": company.vacancy_set.count})
    return lst_company


def get_total_company() -> int:
    """
    Возвращает количество компаний.
    """
    company_count = cache.get("company_count")

    if company_count is None:
        company_count = models.Company.objects.count()
        cache.set("company_count", company_count, 180)

    return company_count


def get_total_vacancy() -> int:
    """
    Возвращает количество вакансий.
    """
    vacancy_count = cache.get("vacancy_count")

    if vacancy_count is None:
        vacancy_count = models.Vacancy.objects.count()
        cache.set("vacancy_count", vacancy_count, 180)

    return vacancy_count
