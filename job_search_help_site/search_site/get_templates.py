from .services import auth


def get_base_template(request):
    """
    Возвращате базовый шаблон от которого будет идти наследование.
    """
    if request.user.is_authenticated:
        user = auth.check_user_role(request)
        if user == "applicant":
            template_name = "base_applicant.html"
        elif user == "company":
            template_name = "employer.html"
    else:
        template_name = "base.html"
    return template_name
