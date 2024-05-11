from typing import Any

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from search_site.get_templates import get_base_template


class CookieForGetTemplate:
    """
    Class for get/set in cookie name of base template by user role.
    """

    @staticmethod
    def process_cookie(request: HttpRequest, template_name: str, other_data: dict = None, max_age=60):
        if other_data is None:
            other_data = {}
        value_cookie = get_base_template(request)
        response = render(request, template_name, {"template": value_cookie, **other_data})
        response = CookieForGetTemplate.set_process_cookie(response, "template", value_cookie, max_age=max_age)
        return response

    @staticmethod
    def set_process_cookie(response: HttpResponse, name_cookie: str, value_cookie: Any, max_age: int):
        response.set_cookie(name_cookie, value_cookie, max_age=max_age)
        return response
