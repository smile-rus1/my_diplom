from search_site import models


def get_all_responses_on_vacancy(user: models.CustomUser) -> models.Application:
    return models.Application.objects.filter(applicant__user=user).prefetch_related("applicant")


def get_filter_responses(response: models.Application, status: str) -> models.Application:
    return response.filter(status=status)
