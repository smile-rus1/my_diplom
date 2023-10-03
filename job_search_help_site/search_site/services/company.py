from search_site import models


def get_all_company() -> list[models.Company]:
    """
    Возвращает все компании.
    """
    # потом сделать фильты, по типу:
    # фильтр по большинству вакансий, или сортировка по алфавитному порядку и т.п.
    return models.Company.objects.all()
