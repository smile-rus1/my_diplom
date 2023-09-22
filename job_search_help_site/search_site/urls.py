from django.urls import path
from . import views


urlpatterns = [
    # общие urlы
    path("", views.index, name="index"),
    path("logout/", views.logout_user, name="logout_user"),
    path("help/", views.help_for_people, name="help"),
    path("delete_me/", views.delete_me, name="delete_me"),

    # для applicant
    path("login/applicant", views.login_applicant, name="login_applicant"),
    path("register/applicant", views.register_applicant, name="register_applicant"),
    path("applicant/", views.main_applicant, name="main_applicant"),
    path("applicant/resumes", views.resumes_applicant, name="rezume_applicant"),
    path("applicant/home_page", views.applicant_home_page, name="applicant_home_page"),
    path("applicant/home_page/change_password", views.change_password, name="change_password_applicant"),
    path("applicant/create_resume", views.create_resume, name="create_resume"),
    path("applicant/delete_resume/<int:resume_id>", views.delete_resume, name="delete_resume"),
    path("applicant/update_resume/<int:resume_id>", views.update_resume, name="update_resume"),
    path("vacancy/<int:vacancy_id>", views.vacancy_for_applicant, name="vacancy"),
    path("applicant/responses/", views.respond_on_vacancy_applicant, name="all_respond_on_vacancy"),
    path("applicant/search/", views.search_vacancy, name="search_vacancy"),

    # url для employer
    path("employer/", views.index_employer, name="employer"),
    path("login/employer", views.login_employer, name="login_employer"),
    path("register/employer", views.register_employer, name="register_employer"),
    path("employer/main", views.main_employer, name="main_employer"),
    path("employer/vacancy", views.vacancy_company, name="vacancy_company"),
    path("employer/create_vacancy", views.create_vacancy, name="create_vacancy"),
    path("employer/update_vacancy/<int:vacancy_id>", views.update_vacancy, name="update_vacancy"),
    path("employer/change_published/<int:vacancy_id>", views.change_published_vacancy, name="change_published"),
    path("employer/delete_vacancy/<int:vacancy_id>", views.delete_vacancy, name="delete_vacancy"),
    path("employer/home_page", views.home_page_company, name="company_home_page"),
    path("employer/home_page/change_password", views.change_password, name="change_password_employer"),
    path("employer/responses/", views.responded_to_vacancy, name="responded_to_vacancy"),
    path("employer/responses/<int:applicant_id>/<int:vacancy_id>", views.show_info_about_applicant_of_application, name="show_info_of_applicant"),
    path("employer/change_state/<int:application_id>", views.change_state_application_of_applicant, name="change_state"),
    path("employer/search/", views.search_resume, name="search_resume"),

    # url для admin
    path('admin_redirect/', views.admin_redirect, name='admin')
]
