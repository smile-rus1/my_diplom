from django.db.models import Q

from search_site import models


def get_all_desired_vacancy(resume: models.Resume) -> Q:
    """
    Возвращает все вакасии, которые подходят по переданному резюме.
    """
    queries = Q()
    queries |= _get_vacancy_by_key_skills(resume.key_skills, queries)
    queries |= _get_vacancy_by_title_vacancy(resume.name_of_resume, queries)
    queries |= _get_vacancy_by_description(resume.about_applicant, queries)
    queries &= Q(is_published=True)

    return queries


def _get_vacancy_by_key_skills(key_skills: str, queries: Q) -> Q:
    """
    Объединяет и возвращает вакансии по совпадению "key_skills".
    """
    for key in key_skills.split(","):
        queries |= Q(key_skills__icontains=key.strip())
    return queries


def _get_vacancy_by_title_vacancy(name_of_resume: str, queries: Q) -> Q:
    """
    Объединяет и возвращает вакансии по совпадению "title_vacancy".
    """
    for name in name_of_resume.split(" "):
        queries |= Q(title_vacancy__icontains=name.strip())
    return queries


def _get_vacancy_by_description(about_applicant: str, queries: Q) -> Q:
    """
     Объединяет и возвращает вакансии по совпадению "description".
    """
    for descr in about_applicant.split(" "):
        queries |= Q(description__icontains=descr.strip())
    return queries
