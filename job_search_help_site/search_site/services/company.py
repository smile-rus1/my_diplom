import re

from django.db.models import Q
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


def get_company_by_letter(letter: str) -> list[models.Company]:
    """
    Получает компании по переданной букве в URL.
    """
    if letter == "NUMBER":
        q = _get_q_obj_by_number_of_letter()
        return models.Company.objects.filter(q).order_by("title_company")

    if not _is_correct_letter(letter):
        return get_all_company()

    return models.Company.objects.filter(title_company__istartswith=letter).order_by("title_company")


def _is_correct_letter(letter: str) -> bool:
    """
    Проверка корректности ввода letter в URL.
    """
    if not re.match(r'^[а-яА-Яa-zA-Z]$', letter):
        return False
    if not (re.match(r'[а-яА-Я]', letter, re.IGNORECASE) or re.match(r'[a-zA-Z]', letter)):
        return False

    return True


def _get_q_obj_by_number_of_letter() -> Q:
    """
    Получаем Q-объект, для фильтрации компании.
    """
    q = Q(title_company__istartswith="0") | Q(title_company__istartswith="1") | Q(title_company__istartswith="2") | \
        Q(title_company__istartswith="3") | Q(title_company__istartswith="4") | Q(title_company__istartswith="5") | \
        Q(title_company__istartswith="6") | Q(title_company__istartswith="7") | Q(title_company__istartswith="8") | \
        Q(title_company__istartswith="9")

    return q

