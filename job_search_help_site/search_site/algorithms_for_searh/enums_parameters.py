from enum import Enum


class EmploymentType(Enum):
    """
    Перечисление для выбора типа занятости.
    """

    PART_TIME = "Подработка"
    PART_EMPLOYMENT = "Частичная занятость"
    FULL_TIME = "Полный рабочий день"
    INTERNSHIP = "Стажировка"
    DISTANT_WORK = "Удаленная работа"
    SHIFT_WORK = "Вахтовый метод работы"
    SEASON_WORK = "Сезонная работа"
    CONTRACT_WORK = "Контрактная работа"


class SpecializationType(Enum):
    """
    Перечисление для выбора специализации.
    """

    PRODUCTION_MANUFACTURING = "Производство и изготовление"
    FINANCE_INVESTMENTS = "Финансы и инвестиции"
    MEDICINE_HEALTHCARE = "Медицина и здравоохранение"
    EDUCATION = "Образование"
    TRANSPORT_LOGISTIC = "Транспорт и логистика"
    INFORMATION_TECHNOLOGY = "Информационные технологии"
    MARKETING_ADVERTISING = "Маркетинг и реклама"
    RETAIL = "Розничная торговля"


class ExperienceType(Enum):
    """
    Перечисление для выбора опыта работы
    """

    NO_EXPERIENCE = ""
    BETWEEN_ONE_AND_THREE = "1 AND 3"
    BETWEEN_THREE_AND_FIVE = "3 AND 5"
    MORE_THEN_FIVE = "MORE 5"


class PublicationTimeType(Enum):
    """
    Перечисление для выбора вывода по времени вакансий.
    """

    ALL_TIME = "ALL_TIME"
    LAST_MONTH = "LAST_MONTH"
    LAST_WEEK = "LAST_WEEK"
    LAST_THREE_DAYS = "LAST_THREE_DAYS"
    LAST_DAY = "LAST_DAY"


class ProfessionType(Enum):
    """
    Перечисление для выбора профессий.
    """

    NO_PROFESSION = "Нет профессии"
    DEVELOPER = "Разработчик"
    DESIGNER = "Дизайнер"
    MANAGER = "Менеджер"
    SECURITY = "Охранник"
    COURIER = "Курьер"
    DRIVER = "Водитель"
    ADMINISTRATOR = "Администратор"
    SECRETARY = "Секретарь"
    COOK = "Повар"
    SWAMPER = "Разнорабочий"
    ASSISTANT = "Помощник"


class EducationType(Enum):
    """
    Перечисление для выбора образования.
    """
    NO_EDUCATION = "Нет образования"
    AVERAGE = "Среднее"
    SPECIALIZED_SECONDARY = "Среднее специальное"
    INCOMPLETE_HIGHER = "Неоконченное высшее"
    HIGHER = "Высшее"
    BACHELOR = "Бакалавр"
    MASTER = "Магистр"
    PHD = "Кандидат наук"
    DOCTOR_SCIENCE = "Доктор наук"
