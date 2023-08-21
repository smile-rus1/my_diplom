from django.core.exceptions import ValidationError

from . import validators
from search_site import models
from .home_page import get_company


def create_vacancy_company(user: models.CustomUser, vacancy_data: dict):
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


def get_all_vacancy_company(user: models.CustomUser) -> list[models.Vacancy]:
    return models.Vacancy.objects.filter(company=(get_company(user)).id)
