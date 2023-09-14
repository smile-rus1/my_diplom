from django.core.paginator import Paginator

from search_site import models


def create_pagination_for_applicant_search(vacancies: models.Vacancy) -> Paginator:
    """
    Создает пагинатор для страницы поиска для кандидата.
    """
    return Paginator(vacancies, 20)
