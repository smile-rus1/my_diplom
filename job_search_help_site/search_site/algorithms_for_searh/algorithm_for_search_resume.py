from django.db.models import Q

from search_site import models
from ._algorithms_of_search import search_resume


def get_all_resume_by_criterion(criteria: str) -> models.Resume:
    """
    Возвращает все Resume, в которых находятся эти критерии, которые
    были переданы.
    """
    if criteria == "ALL_RESUME":
        return search_resume.get_all_model()
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


def get_resumes_by_parameters(request) -> models.Resume:
    """
    Возвращает резюме по переданным в URL
    заголовкам/параметрам.
    """
    combined_resume = None

    if request.GET.get("experience"):
        query = search_resume.get_resumes_by_experience(request.GET.get("experience"))
        if combined_resume is None:
            combined_resume = query
        else:
            combined_resume = [resume for resume in combined_resume if resume in query]

    if request.GET.get("profession"):
        query = search_resume.get_resumes_by_profession(request.GET.get("profession"))
        if combined_resume is None:
            combined_resume = query
        else:
            combined_resume = [resume for resume in combined_resume if resume in query]

    if request.GET.get("education"):
        query = search_resume.get_resume_by_education(request.GET.get("education"))
        if combined_resume is None:
            combined_resume = query
        else:
            combined_resume = [resume for resume in combined_resume if resume in query]

    if combined_resume is None:
        return ""
    return combined_resume
