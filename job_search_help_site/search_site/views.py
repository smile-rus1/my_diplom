from django.contrib.auth import logout
from django.http import HttpResponseRedirect, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.core.cache import cache

from .services import auth, home_page, resume, vacancy, response_for_applicant, responses_on_vacancy, \
    responded_to_vacancy_of_applicant, resume_of_applicants_for_company, applications, popular_company, company

from .algorithms_for_searh import algorithm_for_search_vacancy, algorithm_for_search_resume
from . import pagination_for_pages, get_templates, enums
from .messages import send_help_message
from job_search_help_site import settings


def page_not_found(request, exception):
    return render(request, 'NOTFOUND.html', {"template": get_templates.get_base_template(request)}, status=404)


def index(request):
    """
    Начальная страница на сайте.
    """
    return render(
        request,
        "index.html",
        {
            "popular_company": popular_company.get_lst_company_data(
                popular_company.get_most_popular_company_on_total_vacancy()[:5]
            ),
            "count_company": popular_company.get_total_company(),
            "count_vacancy": popular_company.get_total_vacancy(),
        }
    )


def help_for_people(request):
    """
    Страница help для user
    """
    return render(
        request,
        "help.html",
        {
            "template": get_templates.get_base_template(request),
            "success": request.session.get('message', '') if request.session.get('message', '') else None
        }
    )


def register_confirm(request, token):
    """
    Потверждение регистрации от пользователей.
    """
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    user_info = cache.get(redis_key) or {}
    user_role = user_info.get("role") or {}

    if user_id := user_info.get("user_id"):
        if auth.is_confirmation_user(request, user_id):
            if user_role == "applicant":
                return redirect(to=reverse_lazy("main_applicant"))
            elif user_role == "company":
                return redirect(to=reverse_lazy("main_employer"))
            else:
                return redirect(to=reverse_lazy("index"))
    else:
        if user_role == "applicant":
            return redirect(to=reverse_lazy("register_applicant"))
        elif user_role == "company":
            return redirect(to=reverse_lazy("register_employer"))

    return redirect("index")


def login_applicant(request):
    """
    Авторизация кандидата по url login/applicant.
    """
    if request.method == 'POST':
        if not auth.login_user(
                request,
                {
                    "email": request.POST.get('email'),
                    "password": request.POST.get('password')
                }
        ):
            return render(request, 'login_applicant.html', {'error_message': "Неправильный email или пароль!"})
        else:
            return redirect("main_applicant")

    return render(request, "login_applicant.html")


def register_applicant(request):
    """
    Регистрация кандидата по url register/applicant
    еще будет меняться т.к. не настроил модельки еще!
    """
    if request.method == "POST":
        if not auth.register_user(
                request,
                request.POST.get("email"),
                request.POST.get("password1"),
                request.POST.get("password2"),
                "applicant"
        ):
            return redirect("register_applicant")
        else:
            return redirect("register_applicant")

    return render(request, "register_applicant.html")


def index_employer(request):
    """
    Возвращает страницу для просмотра компаний.
    """
    return render(request, "index_employer.html")


def login_employer(request):
    """
    Авторизация employer по email и password.
    В будующем думаю отрефакторить, сделать один обработчик, чтобы она авторизировала и applicant,
    и company.
    Примерно так =>
    exists, type = auth.login_user(....) => auth.login_user будет возвращать
    --- существует пользователь и тип, и от типа будет зависеть куда перенаправлять.
     print(request.path_info)
    if request.path_info == "/register/employer": --- можно через пути как-то сделать чтобы один обработчик
    только был
        print('!!!!!!!!')
    """
    if request.method == "POST":
        if not auth.login_user(
                request,
                {
                    "email": request.POST.get("email"),
                    "password": request.POST.get("password")
                }
        ):
            return render(request, "login_employer.html", {'error_message': "Неправильный email или пароль!"})
        else:
            return redirect("main_applicant")

    return render(request, "login_employer.html")


def register_employer(request):
    """
    Регистрация employer.
    """
    if request.method == "POST":

        if not auth.register_user(
                request, request.POST.get("email"),
                request.POST.get("password1"),
                request.POST.get("password2"),
                "company"
        ):
            return redirect("register_employer")
        else:
            return redirect("register_employer")

    return render(request, "register_employer.html")


def admin_redirect(request):
    """
    Переводит на админ-панель.
    """
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))


def main_employer(request):
    """
    Возвращате гланую страницу для компаний.
    """
    resumes = resume_of_applicants_for_company.get_resume_for_company_by_algorithm_in_main_page(request.user)

    return render(
        request,
        "index_company.html",
        {
            "resumes": resumes,
            "popular_company": popular_company.get_lst_company_data(
                popular_company.get_most_popular_company_on_total_vacancy()[:5]
            )
        }
    )


def logout_user(request):
    try:
        if request.user.company:
            logout(request)
            return redirect("employer")
    except:
        logout(request)
        return redirect("index")


def main_applicant(request):
    """
    Главная страница для кандидатов
    """
    if not home_page.get_applicant(request.user):
        return redirect("main_employer")
    return render(
        request,
        "index_applicant.html",
        {
            "vacancies": vacancy.get_vacancy_by_algorithm_on_main_page(request.user),
            "popular_company": popular_company.get_lst_company_data(
                popular_company.get_most_popular_company_on_total_vacancy()[:5]
            )
        }
    )


def search_vacancy(request):
    """
    Ищет вакансии по введенному значению от кандидата.
    """
    if [param for param in enums.RequestSearchVacancyParameters if request.GET.get(param.value)]:
        vacancies = algorithm_for_search_vacancy.get_vacancies_by_parameters(request)
    else:
        vacancies = algorithm_for_search_vacancy.get_all_vacancy_by_criterion(request.GET.get("vacancy"))
    paginator = pagination_for_pages.create_pagination_for_search(vacancies)
    return render(
        request,
        "list_vacancy_for_applicant.html",
        {
            "template": get_templates.get_base_template(request),
            "page": paginator.get_page(request.GET.get("page")),
            "selector": {  # в будующем мб вынести в dict-compr т.к. это бизнес-логика c помощью Enums
                "time_employment": request.GET.get("time_employment", ""),
                "specialization": request.GET.get("specialization", ""),
                "experience": request.GET.get("experience", ""),
                "date_publication": request.GET.get("date_publication", "")
                         }
        }
    )


def resumes_applicant(request):
    """
    Страница для applicant, где создается и выводиться резюме.
    """
    return render(request, "applicant_resumes.html", {"resumes": resume.get_all_resumes(request.user)})


def change_published_resume(request, resume_id: int):
    """
    Изменяет видимость резюме.
    """
    if request.method == "POST":
        resume.change_published_resume(request.user, resume_id)
    return redirect("rezume_applicant")


def applicant_home_page(request):
    """
    Домашняя страница applicant, где можно изменить информацию об applicant.
    """
    if request.method == "POST":
        if home_page.change_info_about_applicant(
                request.user,
                {
                    "email": request.POST.get('email'),
                    "first_name": request.POST.get("first_name"),
                    "second_name": request.POST.get("second_name"),
                    "phone": request.POST.get("phone"),
                    "photo": request.FILES.get('image') if request.FILES.get("image") else None
                }
        ):
            return render(request, "home_page_applicant.html", {"alert": True})
        else:
            return render(request, "home_page_applicant.html",
                          {"error_message": "Ошибка, такой телефон уже есть!"}
                          )

    return render(request, "home_page_applicant.html", {"applicant": home_page.get_applicant(request.user)})


def change_password(request):
    """
    Страница на которой пользователь изменяет свой пароль.
    """
    template = get_templates.get_base_template(request)

    if request.method == "POST":
        if request.POST.get("password1") == request.POST.get("password2"):
            if not home_page.user_change_password(
                    request,
                    request.user,
                    {
                        "current_password": request.POST.get("password"),
                        "new_password": request.POST.get("password1")
                    }
            ):
                return render(request, "change_password.html", {'error_message': "Не правильно введен пароль!",
                                                                "template": template})
            else:
                return render(request, "change_password.html", {'successful_message': "Пароль изменен!",
                                                                "template": template})

        else:
            return render(request, 'change_password.html', {'error_message': "Пароли не совпадают!",
                                                            "template": template})

    return render(request, "change_password.html", {"template": template})


def create_resume(request):
    """
    Создание резюме кандидата.
    """
    if request.method == "POST":
        if not resume.create_resume_applicant(
                request.user,
                {
                    "gender": request.POST.get("gender"),
                    "name_of_resume": request.POST.get("name_resume"),
                    "education": request.POST.get("education"),
                    "about_applicant": request.POST.get("about_applicant"),
                    "profession": request.POST.get("profession"),
                    "key_skills": request.POST.get("skills"),
                    "place_of_work": request.POST.get("workplace"),
                    "experience": request.POST.get("experience"),
                    "salary": request.POST.get("salary"),
                    "currency": request.POST.get("currency")
                }
        ):
            return render(request, "create_resume.html", {"error_message": "Некорректно введены данные!"})
        return redirect("rezume_applicant")

    return render(request, "create_resume.html")


def delete_resume(request, resume_id: int):
    """
    Удаляет резюме кандидата.

    """
    if request.method == "POST":
        resume.delete_resume(request.user, resume_id)
    return redirect("rezume_applicant")


def update_resume(request, resume_id: int):
    """
    Обновление резюме кандидата.
    """
    if resume.get_resume(request.user, resume_id) is None:
        return redirect("rezume_applicant")

    if request.method == "POST":
        if not resume.update_resume(
                request.user,
                resume_id,
                {
                    "gender": request.POST.get("gender"),
                    "name_of_resume": request.POST.get("name_resume"),
                    "education": request.POST.get("education"),
                    "about_applicant": request.POST.get("about_applicant"),
                    "profession": request.POST.get("profession"),
                    "key_skills": request.POST.get("skills"),
                    "place_of_work": request.POST.get("workplace"),
                    "experience": request.POST.get("experience"),
                    "salary": request.POST.get("salary"),
                    "currency": request.POST.get("currency")
                }
        ):
            return render(request, "create_resume.html", {
                "resume": resume.get_resume(request.user, resume_id),
                "error_message": "Не правильно введены данные, или что-то пошло не так!"
            })
        else:
            return redirect("rezume_applicant")

    return render(request, "create_resume.html", {"resume": resume.get_resume(request.user, resume_id)})


def vacancy_for_applicant(request, vacancy_id):
    """
    Возвращает страницу вакансий для кандидатов.
    P.S. Переделать эту вьюху чтобы не была такая большая.
    """
    if request.method == "POST":
        application = response_for_applicant.respond_on_vacancy(
            request.user,
            vacancy_id,
            request.POST.get("covering_letter"),
            request.POST.get("resumes_of_applicant")
        )
        if application is None:
            return render(request, "vacancy_for_applicant.html",
                          {
                              "vacancy": vacancy.get_vacancy_by_id(vacancy_id),
                              "error_message": "У вас нет ни одного резюме, создайте хотя-бы одно!"
                          }
                          )
        return HttpResponseRedirect(request.path)

    return render(request, "vacancy_for_applicant.html",
                  {
                      "vacancy": vacancy.get_vacancy_by_id(vacancy_id),
                      "resumes": resume.get_all_resumes(request.user),
                      "apply": response_for_applicant.is_has_applied_respond(request.user, vacancy_id),
                  }
                  )


def respond_on_vacancy_applicant(request):
    """
    Возвращает вакансии на которые был подан отклик.
    """
    user_responses = responses_on_vacancy.get_all_responses_on_vacancy(request.user)
    status = request.GET.get('status', '')
    if status:
        status = request.GET.get('status')
        user_responses = responses_on_vacancy.get_filter_responses(user_responses, status)
    return render(
        request,
        "respond_on_vacancy.html",
        {
            "status": status,
            "responses": user_responses
        }
    )


def vacancy_company(request):
    """
    Страница для company, где создается и выводится vacancy.
    """
    return render(request, "company_vacancy.html", {"vacancies": vacancy.get_all_vacancy_company(request.user)})


def create_vacancy(request):
    """
    Страница для создания vacancy для company.
    """
    if request.method == "POST":
        if not vacancy.create_vacancy_company(
                request.user,
                {
                    "title_vacancy": request.POST.get("title_vacancy"),
                    "location": request.POST.get("location"),
                    "type_of_employment": request.POST.get("type_of_employment"),
                    "specialization": request.POST.get("specialization"),
                    "salary": request.POST.get("salary"),
                    "currency": request.POST.get("currency"),
                    "experience": request.POST.get("experience"),
                    "key_skills": request.POST.get("key_skills"),
                    "description": request.POST.get("descriptions"),
                    "is_published": True if request.POST.get("is_published") else False
                }
        ):
            return render(request, "create_vacancy.html", {"error_message": "Некорректно введены данные!"})

        return redirect("vacancy_company")

    return render(request, "create_vacancy.html")


def update_vacancy(request, vacancy_id: int):
    """
    Обновляет vacancy компании по vacancy_id.
    Позже сделать так, чтобы взаместо 404 ошибка, переводило на главную страницу.
    """
    if vacancy.get_vacancy_for_company(request.user, vacancy_id) is None:
        return redirect("vacancy_company")

    if request.method == "POST":
        if not vacancy.update_vacancy(
                request.user,
                vacancy_id,
                {
                    "title_vacancy": request.POST.get("title_vacancy"),
                    "location": request.POST.get("location"),
                    "type_of_employment": request.POST.get("type_of_employment"),
                    "specialization": request.POST.get("specialization"),
                    "salary": request.POST.get("salary"),
                    "currency": request.POST.get("currency"),
                    "experience": request.POST.get("experience"),
                    "key_skills": request.POST.get("key_skills"),
                    "description": request.POST.get("descriptions"),
                    "is_published": True if request.POST.get("is_published") else False
                }
        ):
            return render(request, "create_vacancy.html", {
                "vacancy": vacancy.get_vacancy_for_company(request.user, vacancy_id),
                "error_message": "Не правильно введены данные, или что-то пошло не так!"
            })
        else:
            return redirect("vacancy_company")

    return render(
        request,
        "create_vacancy.html",
        {
            "vacancy": vacancy.get_vacancy_for_company(request.user, vacancy_id)
        }
                )


def change_published_vacancy(request, vacancy_id: int):
    """
    Изменяет видимость vacancy для applicant.
    """
    if request.method == "POST":
        vacancy.change_published_vacancy(request.user, vacancy_id)
    return redirect("vacancy_company")


def delete_vacancy(request, vacancy_id: int):
    """
    Удаляет вакансию company.
    """
    if request.method == "POST":
        vacancy.delete_vacancy(request.user, vacancy_id)
    return redirect("vacancy_company")


def home_page_company(request):
    """
    Домашняя страница компании, где можно поменять информацию о комнпании.
    """
    if request.method == "POST":
        if home_page.change_info_about_company(
                request.user,
                {
                    "email": request.POST.get("email"),
                    "name_user": request.POST.get("name_user"),
                    "second_name_user": request.POST.get("second_name_user"),
                    "title_company": request.POST.get("title_company"),
                    "phone_company": request.POST.get("phone_company"),
                    "description_company": request.POST.get("description_company"),
                    "image_company": request.FILES.get("image_company") if request.FILES.get("image_company") else None
                }
        ):
            return render(request, "home_page_company.html", {"alert": True})
        else:
            return render(request, "home_page_company.html",
                          {"error_message": "Ошибка, такой телефон уже есть!"}
                          )

    return render(request, "home_page_company.html", {"company": home_page.get_company(request.user)})


def delete_me(request):
    """
    Удаляет аккаунт пользователя.
    """
    template = get_templates.get_base_template(request)

    if request.method == "POST":
        if not home_page.delete_me(request.user, request.POST.get("password")):
            return render(request, "delete_me.html", {"error_message": "Не правильный пароль",
                                                      "template": template})
        else:
            return redirect("index")

    return render(request, "delete_me.html", {"template": template})


def responded_to_vacancy(request):
    """
    Показывает всех applicant, которые откликнулись на вакансии.
    """
    applications = responded_to_vacancy_of_applicant.get_all_responded_to_vacancy(request.user)
    status = request.GET.get("status", "")
    if status:
        status = request.GET.get("status")
        applications = responses_on_vacancy.get_filter_responses(applications, status)
    return render(
        request,
        "responded_to_vacancy.html",
        {
            "applications": applications,
            "status": status
        }
                )


def show_info_about_applicant_of_application(request, applicant_id: int, vacancy_id: int):
    """
    Показывает резюме кандидата, который откликнулся на вакансию.
    """
    return render(
        request,
        "show_info_about_applicant_of_application.html",
        {
            "info_application": responded_to_vacancy_of_applicant.show_all_info_about_applicant_of_application\
            (
                request.user,
                applicant_id,
                vacancy_id
            )
        }
    )


def change_state_application_of_applicant(request, application_id: int):
    """
    Меняет состояние у applicant (access/reject).
    """
    if request.method == "POST":
        responded_to_vacancy_of_applicant.change_application_status_of_applicant(
            status=request.POST.get("change-state"),
            application_id=application_id
        )
    return redirect("responded_to_vacancy")


def search_resume(request):
    """
    Ищет резюме по введенному значению
    """
    if [param for param in enums.RequestSearchResumeParameters if request.GET.get(param.value)]:
        resumes = algorithm_for_search_resume.get_resumes_by_parameters(request)
    else:
        resumes = algorithm_for_search_resume.get_all_resume_by_criterion(request.GET.get("resume"))
    paginator = pagination_for_pages.create_pagination_for_search(resumes)
    return render(
        request,
        "list_resume_for_company.html",
        {
            "template": get_templates.get_base_template(request),
            "page": paginator.get_page(request.GET.get("page")),
            "selector": {  # в будующем мб вынести в dict-compr т.к. это бизнес-логика c помощью Enums
                "experience": request.GET.get("experience", ""),
                "profession": request.GET.get("profession", ""),
                "education": request.GET.get("education", ""),
                        }
        }
    )


def raising_resume(request, resume_id: int):
    """
    Поднимает резюме в поиске.
    """
    if request.method == "POST":
        resume.change_raising_resume(resume_id)
    return redirect("rezume_applicant")


def raising_vacancy(request, vacancy_id: int):
    """
    Поднимает вакансию компании в поиске.
    """
    if request.method == "POST":
        vacancy.change_raising_vacancy(vacancy_id)
    return redirect("vacancy_company")


def change_vision_application_on_list_of_active(request, application_id: int):
    """
    Пользователь удаляет отклик.
    """
    if request.method == "POST":
        applications.change_application_on_user_of_list_active(application_id)
    return redirect("all_respond_on_vacancy")


def show_info_about_applicant_resume(request, resume_id):
    """
    Компания просматривает резюме кандидата.
    """
    info_applicant = responded_to_vacancy_of_applicant.show_all_info_about_applicant(resume_id)

    return render(
        request,
        "show_info_about_applicant.html",
        {
            "info_applicant": info_applicant,
            "vacancies": vacancy.get_all_vacancy_company(request.user),
            "apply_list_respond": responded_to_vacancy_of_applicant.get_is_applied_respond_from_company(request.user)
        }
    )


def send_invitation_from_the_company(request, resume_id: int):
    """
    Присылает приглашение кандидату
    """
    if request.method == "POST":
        responded_to_vacancy_of_applicant.send_invitation_from_the_company_to_applicant(
            request.user,
            resume_id,
            request.POST.get("title_vacancy")
        )
    return redirect("responded_to_vacancy")


def catalog_of_company(request):
    """
    Выводит каталог всех компаний.
    """
    paginator = pagination_for_pages.pagination_for_catalog_company(company.get_all_company())
    if request.GET.get("letters"):
        paginator = pagination_for_pages.pagination_for_catalog_company(
            company.get_company_by_letter(request.GET.get("letters"))
        )

    return render(
        request,
        "catalog_of_company.html",
        {
            "template": get_templates.get_base_template(request),
            "page": paginator.get_page(request.GET.get("page")),
        }
    )


def show_info_about_company(request, company_id: int):
    """
    Показывает информацию об одной компании.
    """
    company_data = company.get_company_by_id(company_id)
    if company_data is None:
        return HttpResponseNotFound()
    return render(
        request,
        "show_info_about_company.html",
        {
            "template": get_templates.get_base_template(request),
            "company": company_data,
            "all_vacancies": company_data.vacancy_set.all()
        }
    )


def show_vacancy(request, vacancy_id: int):
    """
    Показывает вакансию для пользователя.
    """
    return render(
        request,
        "show_info_about_vacancy.html",
        {
            "template": get_templates.get_base_template(request),
            "vacancy": vacancy.get_vacancy_by_id(vacancy_id)
        }
    )


def send_message_from_help_page(request):
    """
    Отправляет сообщение со страницы help.
    """
    if request.method == "POST":
        if send_help_message.send_message_from_help_page_to_email(
            topic=request.POST.get("otherTopic") if request.POST.get("topic") == "other" else request.POST.get("topic"),
            content=request.POST.get("content"),
            email=request.POST.get("email"),
            fullname=request.POST.get("fullname")
        ):
            request.session['message'] = "Сообщение успешно отправлено"
    return redirect("help")


def clear_session_success_message(request):
    """
    Удаляет сообщение из сессии 'success'
    """
    request.session.pop("message", None)
    return JsonResponse(
        {'message': 'Сообщение удалено из сессии'}
    )


def forgot_password(request):
    """
    Восстановление пароля пользователя.
    """
    if request.method == "POST":
        auth.get_link_forgot_password(request, request.POST.get("email"))
    return render(
        request,
        "page_forgot_password.html",
        {
            "template": get_templates.get_base_template(request)
        }
    )


def recovery_password(request, token):
    """
    Восстановление пароля пользователя.
    """
    redis_key = settings.SOAQAZ_USER_CONFIRMATION_KEY.format(token=token)
    email_info = cache.get(redis_key)
    email_user = email_info.get("email") or {}
    if request.method == "POST":
        if not auth.change_forgot_password(
            request=request,
            email=email_user,
            password1=request.POST.get("password1"),
            password2=request.POST.get("password2")
        ):
            return HttpResponseRedirect(request.path)

        return redirect("login_applicant")

    return render(
        request,
        "page_recovery_password.html",
        {
            "template": get_templates.get_base_template(request)
        }
    )
