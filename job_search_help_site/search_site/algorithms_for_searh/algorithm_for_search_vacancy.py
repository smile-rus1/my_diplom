from datetime import timedelta

from django.db.models import Q
from django.db import connection
from django.utils import timezone

from search_site import models
from . import enums_parameters


def get_all_vacancy_by_criterion(criteria: str) -> models.Vacancy:
    """
    Возвращает все Vacancy, в которых находятся эти критерии, которые
    были переданы.
    """
    if criteria == "ALL_VACANCY":
        return _get_all_vacancy()
    return models.Vacancy.objects.filter(_get_vacancy_by_criteria(criteria), is_published=True)\
        .prefetch_related("company")\
        .order_by("-publication_time", "-created_at")


def _get_vacancy_by_criteria(criteria: str) -> Q:
    """
    Возвращает все вакансии, у которых есть совпадения по критериям.
    """
    q = Q()
    for cr in criteria.split():
        q |= Q(key_skills__icontains=cr.strip()) | Q(company__title_company__icontains=cr.strip()) \
             | Q(specialization__icontains=cr.strip()) | Q(title_vacancy__icontains=cr.strip())
    return q


def _get_all_vacancy() -> models.Vacancy:
    """
    Возвращает все вакансии для страницы applicant/search/
    """
    return models.Vacancy.objects.all()


def get_vacancies_by_parameters(request):
    """
    Возвращает вакансии, по параметрам переданным в
    URL заголовках.
    """
    combined_vacancies = None

    if request.GET.get("time_employment"):
        query = _get_vacancies_by_time_employment(request.GET.get("time_employment"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("specialization"):
        query = _get_vacancies_by_specialization(request.GET.get("specialization"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("experience"):
        query = _get_vacancies_by_experience(request.GET.get("experience"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if request.GET.get("date_publication"):
        query = _get_vacancies_by_publication_time(request.GET.get("date_publication"))
        if combined_vacancies is None:
            combined_vacancies = query
        else:
            combined_vacancies = [vacancy for vacancy in combined_vacancies if vacancy in query]

    if combined_vacancies is None:
        return ""
    return combined_vacancies


def _get_vacancies_by_time_employment(time_employment: str) -> models.Vacancy:
    """
    Возвращает все вакансии, по параметрам time_employment.
    """
    try:
        employment = enums_parameters.EmploymentType[time_employment.upper()].value
    except KeyError:
        return _get_all_vacancy()
    return models.Vacancy.objects.filter(type_of_employment=employment, is_published=True)


def _get_vacancies_by_specialization(specialization: str) -> models.Vacancy:
    """
    Возвращает вакансии по специализации.
    """
    try:
        specialization_type = enums_parameters.SpecializationType[specialization.upper()].value
    except KeyError:
        return _get_all_vacancy()
    return models.Vacancy.objects.filter(specialization=specialization_type, is_published=True)


def _get_vacancies_by_experience(experience: str) -> models.Vacancy:
    """
    Возвращает вакансии, по параметрам experience.

    P.S. Тут есть сырые SQL-запросы, т.к. у experience тип поля в БД VARCHAR!
    """
    try:
        experience_type = enums_parameters.ExperienceType[experience.upper()].value
    except KeyError:
        return _get_all_vacancy()

    if experience_type == enums_parameters.ExperienceType.NO_EXPERIENCE.value:
        # query = Q(experience__isnull=True) | Q(experience=0)
        return models.Vacancy.objects.filter(experience__isnull=True)

    elif experience_type == enums_parameters.ExperienceType.BETWEEN_ONE_AND_THREE.value:
        # Вот такой код не работает, так как надо, нужно или в БД менять тип поля, или
        # шаманить с запросом
        # query = Q(experience__gte=1) & Q(experience__lte=3)

        with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
            cursor.execute("SELECT * FROM search_site_vacancy WHERE experience >= 1 AND experience <= 3;")
            results = cursor.fetchall()

        vacancy_objects = []
        for data in results:
            vacancy = models.Vacancy(
                id=data[0],
                experience=data[2],
                salary=data[1],
                description=data[3],
                created_at=data[4],
                publication_time=data[5],
                location=data[6],
                company=models.Company.objects.get(id=data[7]),
                specialization=data[8],
                type_of_employment=data[9],
                is_published=data[10],
                key_skills=data[11],
                title_vacancy=data[12]
            )
            vacancy_objects.append(vacancy)

    elif experience_type == enums_parameters.ExperienceType.BETWEEN_THREE_AND_FIVE.value:
        return models.Vacancy.objects.filter(experience__gte=3, experience__lte=5)

    elif experience_type == enums_parameters.ExperienceType.MORE_THEN_FIVE.value:
        with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
            cursor.execute("SELECT * FROM search_site_vacancy WHERE experience > 5")
            results = cursor.fetchall()
        vacancy_objects = []
        for data in results:
            vacancy = models.Vacancy(
                id=data[0],
                experience=data[1],
                salary=data[2],
                description=data[3],
                created_at=data[4],
                publication_time=data[5],
                location=data[6],
                company=models.Company.objects.get(id=data[7]),
                specialization=data[8],
                type_of_employment=data[9],
                is_published=data[10],
                key_skills=data[11],
                title_vacancy=data[12]
            )
            vacancy_objects.append(vacancy)

    queryset = models.Vacancy.objects.none()
    for obj in vacancy_objects:
        queryset |= models.Vacancy.objects.filter(pk=obj.pk)
    return queryset


def _get_vacancies_by_publication_time(time: str) -> models.Vacancy:
    """
    Возвращает все вакансии, по параметрам time.
    """
    now = timezone.now()
    start_time = now
    if time == enums_parameters.PublicationTimeType.ALL_TIME.value:
        start_time = Q(created_at__lte=now)
    elif time == enums_parameters.PublicationTimeType.LAST_MONTH.value:
        start_time = now - timedelta(days=30)
    elif time == enums_parameters.PublicationTimeType.LAST_WEEK.value:
        start_time = now - timedelta(weeks=1)
    elif time == enums_parameters.PublicationTimeType.LAST_THREE_DAYS.value:
        start_time = now - timedelta(days=3)
    elif time == enums_parameters.PublicationTimeType.LAST_DAY.value:
        start_time = now - timedelta(days=1)

    return models.Vacancy.objects.filter(created_at__range=[start_time, now], is_published=True)
