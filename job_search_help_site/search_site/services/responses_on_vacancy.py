from search_site import models
from django.core.cache import cache


def get_all_responses_on_vacancy(user: models.CustomUser) -> models.Application:
    return models.Application.objects.filter(applicant__user=user).prefetch_related("applicant")\
        .order_by("-application_date")


def get_filter_responses(response: models.Application, status: str) -> models.Application:
    return response.filter(status=status)


def get_total_responses(responses: models.Application) -> int:
    """
    Возвращает количество всех откликов на вакансий.
    """
    count_responses = cache.get("count_responses")
    if count_responses is None:
        count_responses = responses.count()
        cache.set("count_responses", count_responses, 300)

    return count_responses
