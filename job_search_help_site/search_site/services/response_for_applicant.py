from search_site import models


def respond_on_vacancy(user: models.CustomUser, vacancy_id: int, cover_letter: str):
    """
    Applicant откликается на вакансию company.
    """
    applicant = models.Applicant.objects.get(user=user)
    vacancy = models.Vacancy.objects.get(pk=vacancy_id)

    models.Application.objects.create(
        applicant=applicant,
        vacancy=vacancy,
        cover_letter=cover_letter,
        company=vacancy.company.title_company
    )


def get_has_applied_respond(user: models.CustomUser, vacancy):
    return models.Application.objects.filter(applicant=models.Applicant.objects.get(user=user),
                                             vacancy=vacancy).exists()


