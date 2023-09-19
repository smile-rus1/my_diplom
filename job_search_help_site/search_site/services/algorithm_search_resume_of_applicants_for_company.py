from django.db.models import Q

from search_site import models


def get_all_desired_resume_of_applicants(vacancy: models.Vacancy) -> Q:
    """
    Возвращает все резюме кандидатов, которые подходят
    по требованиям переданной вакансии.
    """
    queries = Q()
    queries |= _get_resume_by_key_skills(vacancy.key_skills, queries)
    queries |= _get_resume_by_description(vacancy.description, queries)
    queries |= _get_resume_by_name_of_resume(vacancy.title_vacancy, queries)
    queries |= _get_resume_by_salary(
        int(vacancy.salary[:-4]),
        int(vacancy.salary[:-4]) // 4,
        queries
    )
    queries &= Q(is_published=True)
    return queries


def _get_resume_by_key_skills(key_skills: str, queries: Q) -> Q:
    """
    Возвращает резюме, у которых есть совпадения по key_skills.
    """
    for key in key_skills.split(","):
        queries |= Q(key_skills__icontains=key.strip())
    return queries


def _get_resume_by_description(description: str, queries: Q) -> Q:
    """
    Возвращает резюме, у которых есть сопадения по description.
    """
    for descr in description.split():
        queries |= Q(about_applicant__icontains=descr.strip())
    return queries


def _get_resume_by_name_of_resume(title: str, queries: Q) -> Q:
    """
    Возвращает резюме, у которых есть сопадения по name.
    """
    for word in title.split():
        queries |= Q(name_of_resume__icontains=word.strip())
    return queries


def _get_resume_by_salary(vacancy_salary: int, resume_salary: int, queries: Q) -> Q:
    """
    Возвращает резюме, у которых есть сопадения по salary.
    """
    queries |= Q(salary__gte=resume_salary) | Q(salary__lte=vacancy_salary)
    return queries
