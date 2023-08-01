from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("help/", views.help_for_people, name="help"),
    path("login/applicant", views.login_applicant, name="login_applicant"),
    path("register/applicant", views.register_applicant, name="register_applicant"),

    # url для employer
    path("employer/", views.index_employer, name="employer"),
    path("login/employer", views.login_employer, name="login_employer"),
    path("register/employer", views.register_employer, name="register_employer"),
]
