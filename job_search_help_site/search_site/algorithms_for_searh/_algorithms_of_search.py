from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any

from django.db.models import Q
from django.utils import timezone
from django.db import connection

from search_site import models
from . import enums_parameters


class ParentAlgorithmSearch(ABC):
    """
    Класс, который будет задавать общуюу логику для
    других классов-поисков.
    """

    def __init__(self, model_name) -> None:
        self.model_name = model_name

    @abstractmethod
    def get_all_model(self) -> Any:
        """
        Возвращает по переданному model_name значения.
        """
        ...


class SearchVacancy(ParentAlgorithmSearch):
    """
    Класс для алгоритмов поиска вакансий.
    """
    def __init__(self, model_name: models.Vacancy):
        super().__init__(model_name)
        self.model_name = model_name

    def get_all_model(self) -> Any:
        return self.model_name.objects.all()

    def get_vacancies_by_publication_time(self, time: str) -> models.Vacancy:
        """
        Возвращает вакансии соответсвуюущему переданному time-публикации.
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

        return self.model_name.objects.filter(created_at__range=[start_time, now], is_published=True)

    def get_vacancies_by_experience(self, experience: str) -> models.Vacancy:
        """
        Возвращает модельку по переданному experience.

        P.S. Тут есть сырые SQL-запросы, т.к. у experience тип поля в БД VARCHAR!
        """
        try:
            experience_type = enums_parameters.ExperienceType[experience.upper()].value
        except KeyError:
            return self.get_all_model()

        if experience_type == enums_parameters.ExperienceType.NO_EXPERIENCE.value:
            # query = Q(experience__isnull=True) | Q(experience=0)
            return models.Vacancy.objects.filter(experience__isnull=True, is_published=True)

        elif experience_type == enums_parameters.ExperienceType.BETWEEN_ONE_AND_THREE.value:
            # Вот такой код не работает, так как надо, нужно или в БД менять тип поля, или
            # шаманить с запросом
            # query = Q(experience__gte=1) & Q(experience__lte=3)

            with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
                cursor.execute("SELECT * FROM search_site_vacancy WHERE experience >= 1 AND experience <= 3 AND is_published = 1;")
                results = cursor.fetchall()

            vacancy_objects = []
            for data in results:
                vacancy = models.Vacancy(
                    id=data[0],
                    salary=data[1],
                    experience=data[2],
                    title_vacancy=data[3],
                    created_at=data[4],
                    location=data[5],
                    company=models.Company.objects.get(id=data[6]),
                    specialization=data[7],
                    type_of_employment=data[8],
                    is_published=data[9],
                    key_skills=data[10],
                    description=data[11],
                    updated_at=data[12],
                )
                vacancy_objects.append(vacancy)

        elif experience_type == enums_parameters.ExperienceType.BETWEEN_THREE_AND_FIVE.value:
            return models.Vacancy.objects.filter(experience__gte=3, experience__lte=5, is_published=True)

        elif experience_type == enums_parameters.ExperienceType.MORE_THEN_FIVE.value:
            with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
                cursor.execute("SELECT * FROM search_site_vacancy WHERE experience > 5 AND is_published = 1;")
                results = cursor.fetchall()
            vacancy_objects = []
            for data in results:
                vacancy = models.Vacancy(
                    id=data[0],
                    salary=data[1],
                    experience=data[2],
                    title_vacancy=data[3],
                    created_at=data[4],
                    location=data[5],
                    company=models.Company.objects.get(id=data[6]),
                    specialization=data[7],
                    type_of_employment=data[8],
                    is_published=data[9],
                    key_skills=data[10],
                    description=data[11],
                    updated_at=data[12],
                )
                vacancy_objects.append(vacancy)

        queryset = models.Vacancy.objects.none()
        for obj in vacancy_objects:
            queryset |= models.Vacancy.objects.filter(pk=obj.pk)
        return queryset

    def get_vacancies_by_time_employment(self, time_employment: str) -> models.Vacancy:
        """
        Возвращает все вакансии, по параметрам time_employment.
        """
        try:
            employment = enums_parameters.EmploymentType[time_employment.upper()].value
        except KeyError:
            return self.get_all_model()
        return models.Vacancy.objects.filter(type_of_employment=employment, is_published=True)

    def get_vacancies_by_specialization(self, specialization: str) -> models.Vacancy:
        """
        Возвращает вакансии по специализации.
        """
        try:
            specialization_type = enums_parameters.SpecializationType[specialization.upper()].value
        except KeyError:
            return self.get_all_model()
        return models.Vacancy.objects.filter(specialization=specialization_type, is_published=True)


class SearchResume(ParentAlgorithmSearch):
    """
    Класс для алгоритмов поиска резюме.
    """

    def __init__(self, model_name: models.Vacancy):
        super().__init__(model_name)
        self.model_name = model_name

    def get_all_model(self) -> Any:
        return self.model_name.objects.all()

    def get_resumes_by_experience(self, experience: str) -> models.Resume:
        """
        Возвращает модельку по переданному experience.

        P.S. Тут есть сырые SQL-запросы, т.к. у experience тип поля в БД VARCHAR!
        """
        try:
            experience_type = enums_parameters.ExperienceType[experience.upper()].value
        except KeyError:
            return self.get_all_model()

        if experience_type == enums_parameters.ExperienceType.NO_EXPERIENCE.value:
            # query = Q(experience__isnull=True) | Q(experience=0)
            return models.Resume.objects.filter(experience__isnull=True, is_published=True)

        elif experience_type == enums_parameters.ExperienceType.BETWEEN_ONE_AND_THREE.value:
            # Вот такой код не работает, так как надо, нужно или в БД менять тип поля, или
            # шаманить с запросом
            # query = Q(experience__gte=1) & Q(experience__lte=3)

            with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
                cursor.execute("SELECT * FROM search_site_resume WHERE experience >= 1 AND experience <= 3 AND is_published = 1;")
                results = cursor.fetchall()

            resume_objects = []
            for data in results:
                resume = models.Resume(
                    id=data[0],
                    gender=data[1],
                    updated_at=data[2],
                    profession=data[3],
                    applicant=models.Applicant.objects.get(id=data[4]),
                    education=data[5],
                    key_skills=data[6],
                    about_applicant=data[7],
                    experience=data[8],
                    place_of_work=data[9],
                    salary=data[10],
                    name_of_resume=data[11],
                    is_published=data[12],
                )
                resume_objects.append(resume)

        elif experience_type == enums_parameters.ExperienceType.BETWEEN_THREE_AND_FIVE.value:
            return models.Resume.objects.filter(experience__gte=3, experience__lte=5, is_published=True)

        elif experience_type == enums_parameters.ExperienceType.MORE_THEN_FIVE.value:
            with connection.cursor() as cursor:  # тут сырым SQL-запросом, т.к. тип поля у experience VARCHAR
                cursor.execute("SELECT * FROM search_site_resume WHERE experience > 5 AND is_published = 1;")
                results = cursor.fetchall()
            resume_objects = []
            for data in results:
                resume = models.Resume(
                    id=data[0],
                    gender=data[1],
                    updated_at=data[2],
                    profession=data[3],
                    applicant=models.Applicant.objects.get(id=data[4]),
                    education=data[5],
                    key_skills=data[6],
                    about_applicant=data[7],
                    experience=data[8],
                    place_of_work=data[9],
                    salary=data[10],
                    name_of_resume=data[11],
                    is_published=data[12],
                )
                resume_objects.append(resume)

        queryset = models.Resume.objects.none()
        for obj in resume_objects:
            queryset |= models.Resume.objects.filter(pk=obj.pk)
        return queryset

    def get_resumes_by_profession(self, profession: str) -> models.Resume:
        """
        Возвращает резюме по переданному profession.
        """
        try:
            profession_type = enums_parameters.ProfessionType[profession.upper()].value
        except KeyError:
            return self.get_all_model()
        return models.Resume.objects.filter(profession=profession_type, is_published=True)

    def get_resume_by_education(self, education: str) -> models.Resume:
        """
        Возвращает резюме по переданному education.
        """
        try:
            education_type = enums_parameters.EducationType[education.upper()].value
        except KeyError:
            return self.get_all_model()
        return models.Resume.objects.filter(education=education_type, is_published=True)


search_vacancy = SearchVacancy(models.Vacancy)
search_resume = SearchResume(models.Resume)
