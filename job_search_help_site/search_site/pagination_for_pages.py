from typing import Any

from django.core.paginator import Paginator
from . import models


def create_pagination_for_search(data: Any) -> Paginator:
    """
    Создает пагинатор для страницы поиска для кандидата.
    """
    return Paginator(data, 20)


def pagination_for_catalog_company(lst_company: list[models.Company]) -> Paginator:
    """
    Создает пагинатор для страницы каталога компаний.
    """
    return Paginator(lst_company, 21)
