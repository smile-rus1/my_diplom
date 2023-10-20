from enum import Enum


class RequestSearchVacancyParameters(Enum):
    """
    Перчисление для параметров поиска вакансий для кандидата.
    """

    EXPERIENCE = "experience"
    SPECIALIZATION = "specialization"
    TIME_EMPLOYMENT = "time_employment"
    DATE_PUBLICATION = "date_publication"


class RequestSearchResumeParameters(Enum):
    """
    Перечисление для параметров поиска резюме для компаний.
    """

    EXPERIENCE = "experience"
    PROFESSION = "profession"
    EDUCATION = "education"

