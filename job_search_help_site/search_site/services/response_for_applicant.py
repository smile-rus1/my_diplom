from django.urls import reverse_lazy

from search_site import models
from . import send_mail_to_users


def respond_on_vacancy(
        request,
        vacancy_id: int,
        cover_letter: str,
        resume: str
) -> models.Application | None:
    """
    Applicant откликается на вакансию company.
    """
    applicant = models.Applicant.objects.get(user=request.user)
    if not _is_applicant_has_resume(applicant):
        return None

    vacancy = models.Vacancy.objects.get(pk=vacancy_id)
    resume = models.Resume.objects.filter(name_of_resume=resume).first()
    application = models.Application.objects.create(
        applicant=applicant,
        vacancy=vacancy,
        resume=resume,
        cover_letter=cover_letter,
        company=vacancy.company.title_company
    )

    link_to_redirect = request.build_absolute_uri(
        reverse_lazy("show_info_about_applicant_resume", kwargs={"resume_id": resume.id})
    )
    send_mail_to_users.send_mail_to_users(
        subject=f"Кандидат откликнулся на вашу вакансию",
        message=f"Кандидат {applicant.second_name} {applicant.first_name} откликнулся "
                f"на вакансию {vacancy.title_vacancy}"
                f"Ссылка на резюме кандидата: {link_to_redirect}",
        email_recipient=f"{vacancy.company.user.email}"
    )

    return application


def _is_applicant_has_resume(applicant: models.Applicant):
    return models.Resume.objects.filter(applicant=applicant)


def is_has_applied_respond(user: models.CustomUser, vacancy):
    return models.Application.objects.filter(applicant=models.Applicant.objects.get(user=user),
                                             vacancy=vacancy).exists()


