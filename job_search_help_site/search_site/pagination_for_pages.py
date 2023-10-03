from typing import Any

from django.core.paginator import Paginator


def create_pagination_for_search(data: Any) -> Paginator:
    """
    Создает пагинатор для страницы поиска для кандидата.
    """
    return Paginator(data, 20)
