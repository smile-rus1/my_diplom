from django.db.models import Q

from search_site import models


def get_all_desired_resume_of_applicants(vacancy: models.Vacancy) -> models.Resume:
    """
    Возвращает все резюме кандидатов, которые подходят
    по требованиям переданной вакансии.
    """
    queries = Q()

