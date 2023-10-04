from datetime import timedelta

from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import timezone

from . import validators, algorithm_for_vacancy
from search_site import models
from .home_page import get_company


def get_vacancy_by_id(vacancy_id: int) -> models.Vacancy:
    """
    Возвращает vacancy для applicant.
    """
    return get_object_or_404(models.Vacancy, id=vacancy_id)


def get_vacancy_by_algorithm_on_main_page(user: models.CustomUser) -> models.Vacancy:
    """
    Возвращает vacancy, компаний по алгоритму поиска, на главную страницу applicant.
    """
    resume = models.Resume.objects.filter(applicant=get_object_or_404(models.Applicant, user=user))\
        .order_by("?").first()
    if resume is not None:
        vacancies = models.Vacancy.objects.filter(algorithm_for_vacancy.get_all_desired_vacancy(resume))
    else:
        vacancies = models.Vacancy.objects.filter(is_published=True).order_by("?")
    return vacancies[:6]


def get_vacancy_for_company(user: models.CustomUser, vacancy_id: int):
    """
    Возвращает vacancy по его id для компании.
    """
    return _check_and_get_vacancy(user, vacancy_id)


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
    Обновляет vacancy компании по vacancy_id.
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


def change_raising_vacancy(vacancy_id: int) -> None:
    """
    Поднимает вакансию компании в поиске.
    """
    update_interval = timedelta(hours=4)
    vacancy = get_object_or_404(models.Vacancy, pk=vacancy_id)
    current_time = timezone.now()
    cutoff_time = current_time - update_interval

    if vacancy.publication_time.tzinfo is None:
        vacancy.publication_time = timezone.make_aware(vacancy.publication_time)

    if vacancy.publication_time <= cutoff_time:
        vacancy.publication_time = current_time
        vacancy.save()
