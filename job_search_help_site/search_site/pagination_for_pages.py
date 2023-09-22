from django.core.paginator import Paginator

from search_site import models


def create_pagination_for_search(data: models.Vacancy | models.Resume) -> Paginator:
    """
    Создает пагинатор для страницы поиска для кандидата.
    """
    return Paginator(data, 20)
