from django.db.models import Count
from search_site import models


def get_most_popular_company_on_total_vacancy():
    """
    Возвращает популярные компании по кол-ву вакансий.
    """
    return models.Company.objects.annotate(vacancy_count=Count("vacancy")).order_by('-vacancy_count')


def get_lst_company_data(popular_company: models.Company) -> list[models.Company]:
    lst_company: list[dict] = []
    for company in popular_company:
        lst_company.append({"company": company, "vacancy_count": company.vacancy_set.count})
    return lst_company
