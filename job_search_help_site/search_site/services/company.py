from django.shortcuts import get_object_or_404
from search_site import models


def get_all_company() -> list[models.Company]:
    """
    Возвращает все компании.
    """
    # потом сделать фильты, по типу:
    # фильтр по большинству вакансий, или сортировка по алфавитному порядку и т.п.
    return models.Company.objects.all()


def get_company_by_id(company_id: int):
    """
    Возвращает компанию по переданному company_id
    """
    try:
        return models.Company.objects.prefetch_related("vacancy_set").get(id=company_id)
    except models.Company.DoesNotExist:
        return None
