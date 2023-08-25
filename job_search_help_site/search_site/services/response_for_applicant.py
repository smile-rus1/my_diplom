from search_site import models


def respond_on_vacancy(user: models.CustomUser, vacancy_id: int, cover_letter: str) -> models.Application | None:
    """
    Applicant откликается на вакансию company.
    """
    applicant = models.Applicant.objects.get(user=user)
    if not _is_applicant_has_resume(applicant):
        return None

    vacancy = models.Vacancy.objects.get(pk=vacancy_id)
    application = models.Application.objects.create(
        applicant=applicant,
        vacancy=vacancy,
        cover_letter=cover_letter,
        company=vacancy.company.title_company
    )
    return application


def _is_applicant_has_resume(applicant: models.Applicant):
    return models.Resume.objects.filter(applicant=applicant)


def is_has_applied_respond(user: models.CustomUser, vacancy):
    return models.Application.objects.filter(applicant=models.Applicant.objects.get(user=user),
                                             vacancy=vacancy).exists()


