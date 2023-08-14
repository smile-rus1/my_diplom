from django.core.exceptions import ValidationError
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

from search_site import models
from .home_page import get_applicant


def get_resume(user: models.CustomUser) -> list[models.Resume]:
    """
    Возвращает резюме кандидата.
    """
    applicant = get_applicant(user)
    resumes = models.Resume.objects.filter(applicant=applicant.id)
    return resumes


def create_resume_applicant(user: models.CustomUser, resume_data: dict) -> bool:
    """
    Создается резюме кандидата по переданному user и resume_data.
    """
    applicant = get_applicant(user)
    try:
        resume = models.Resume.objects.create(
            applicant=applicant,
            name_of_resume=resume_data.get("name_of_resume"),
            gender=resume_data.get("gender"),
            education=resume_data.get("education"),
            about_applicant=resume_data.get("about_applicant"),
            profession=resume_data.get("profession"),
            key_skills=resume_data.get("key_skills"),
            place_of_work=resume_data.get("place_of_work"),
            experience=_validate_experience(resume_data.get("experience")),
            salary=_validate_salary(resume_data.get("salary"), resume_data.get("currency"))
        )
        return True
    except ValidationError:
        return False


def update_resume():
    ...


def delete_resume(user: models.CustomUser, id_resume: int):
    resume = get_object_or_404(models.Resume, id=id_resume)

    if resume.applicant != get_applicant(user):
        return HttpResponseForbidden("Упс, эта страница не доступна!")

    resume.delete()
    return True


def _validate_salary(salary, currency):
    """
    Валидирует з/п applicanta.
    """
    if salary == "":
        return None

    return salary + " " + currency


def _validate_experience(experience: int) -> str | None:
    """
    Валидирует experience по годам и приставляет суффикс взависимости от кол-ва.
    """
    if not experience:
        return

    experience = int(experience)
    if 1 <= experience <= 4:
        if experience == 1:
            expected_suffix = "год"
        else:
            expected_suffix = "года"
    elif 5 <= experience <= 20:
        expected_suffix = "лет"
    elif 21 <= experience <= 24:
        expected_suffix = "год"
    else:
        raise ValidationError("Некорректный опыт работы")

    return f"{experience} {expected_suffix}"
