from search_site.get_templates import get_base_template


class SessionsForGetTemplate:
    """
    Class for get/set template in session.
    """
    @staticmethod
    def get_template_in_session(request, template_name: str):
        return request.session.get(template_name)

    @staticmethod
    def set_template_in_session(request, template_name: str = "template"):
        value = get_base_template(request)
        request.session[template_name] = value
        return value
