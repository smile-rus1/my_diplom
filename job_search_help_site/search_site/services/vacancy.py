from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from . import validators
from search_site import models
from .home_page import get_company


def _check_and_get_vacancy(user: models.CustomUser, vacancy_id: int) -> models.Vacancy | None:
    """
    Проверяет и возвращает vacancy.
    """
    vacancy = get_object_or_404(models.Vacancy, id=vacancy_id)
    if not _check_is_company(user, vacancy):
        return None
    return vacancy


def _check_is_company(user: models.CustomUser, vacancy: models.Vacancy) -> bool:
    """
    Проверка на то, что изменяет видимость vacancy тот, кто ее создал.
    """
    if vacancy.company != get_company(user):
        return False
    return True


def get_all_vacancy_company(user: models.CustomUser) -> list[models.Vacancy]:
    """
    Возвращает все vacancy компании.
    """
    return models.Vacancy.objects.filter(company=(get_company(user)).id)


def get_vacancy(user: models.CustomUser, vacancy_id: int):
    """
    Возвращает vacancy по его id.
    """
    return _check_and_get_vacancy(user, vacancy_id)


def create_vacancy_company(user: models.CustomUser, vacancy_data: dict) -> bool:
    """
    Создается вакансия компании.
    """

    company = get_company(user)
    try:
        models.Vacancy.objects.create(
            company=company,
            title_vacancy=vacancy_data.get("title_vacancy"),
            location=vacancy_data.get("location"),
            salary=validators.validate_salary(vacancy_data.get("salary"), vacancy_data.get("currency")),
            experience=validators.validate_experience(vacancy_data.get("experience")),
            description=vacancy_data.get("description"),
            type_of_employment=vacancy_data.get("type_of_employment"),
            specialization=vacancy_data.get("specialization"),
            key_skills=vacancy_data.get("key_skills"),
            is_published=vacancy_data.get("is_published")
        )

        return True
    except ValidationError:
        return False


def update_vacancy(user: models.CustomUser, vacancy_id: int, vacancy_data: dict) -> bool | HttpResponseForbidden:
    """
    Обновляет vacancy компании по id_resume.
    """
    vacancy = _check_and_get_vacancy(user, vacancy_id)
    if vacancy is None:
        return HttpResponseForbidden("Упс, эта страница не доступна!")

    models.Vacancy.objects.filter(id=vacancy_id).update(
        title_vacancy=vacancy_data.get("title_vacancy"),
        location=vacancy_data.get("location"),
        salary=validators.validate_salary(vacancy_data.get("salary"), vacancy_data.get("currency")),
        experience=validators.validate_experience(vacancy_data.get("experience")),
        description=vacancy_data.get("description"),
        type_of_employment=vacancy_data.get("type_of_employment"),
        specialization=vacancy_data.get("specialization"),
        key_skills=vacancy_data.get("key_skills"),
        is_published=vacancy_data.get("is_published")
    )
    return True


def change_published_vacancy(user: models.CustomUser, vacancy_id: int) -> HttpResponseForbidden | None:
    """
    Изменяет видимость вакансии комнпаии.
    """
    vacancy = _check_and_get_vacancy(user, vacancy_id)
    if vacancy is None:
        return HttpResponseForbidden("Упс, эта страница не доступна!")
    vacancy.is_published = not vacancy.is_published
    vacancy.save()


def delete_vacancy(user: models.CustomUser, vacancy_id: int) -> HttpResponseForbidden | None:
    """
    Удаляет vacancy у  по vacancy_id.
    """
    vacancy = _check_and_get_vacancy(user, vacancy_id)
    if vacancy is None:
        return HttpResponseForbidden("Упс, эта страница не доступна!")
    vacancy.delete()
