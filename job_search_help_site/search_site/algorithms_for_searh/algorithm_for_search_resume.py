from django.db.models import Q

from search_site import models


def get_all_resume_by_criterion(criteria: str) -> models.Resume:
    """
    Возвращает все Resume, в которых находятся эти критерии, которые
    были переданы.
    """
    return models.Resume.objects.filter(_get_resume_by_criteria(criteria), is_published=True)\
        .prefetch_related("applicant")\
        .order_by("-updated_at")


def _get_resume_by_criteria(criteria: str) -> Q:
    """
    Возвращает все resume, по критериям.
    """
    q = Q()
    for cr in criteria.split():
        q |= Q(name_of_resume__icontains=cr.strip()) | Q(key_skills__icontains=cr.strip()) \
             | Q(about_applicant__icontains=cr.strip()) | Q(profession__icontains=cr.strip())
    return q
