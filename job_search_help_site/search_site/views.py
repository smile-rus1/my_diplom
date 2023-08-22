from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .services import auth, home_page, resume, vacancy


def index(request):
    """
    начальная страница на сайте.
    """
    return render(request, "index.html")


def help_for_people(request):
    """
    Страница help для user
    """
    if request.user.is_authenticated:
        user = auth.check_user_role(request)
        if user == "applicant":
            template_name = "base_applicant.html"
        elif user == "company":
            template_name = "employer.html"

        return render(request, "help.html", {"template": template_name})
    else:
        return render(request, "help.html", {"template": "base.html"})


def login_applicant(request):
    """
    авторизация кандидата по url login/applicant.
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
    регистрация кандидата по url register/applicant
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
            return redirect("main_applicant")

    return render(request, "register_applicant.html")


def index_employer(request):
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
            return redirect("main_employer")

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
            return redirect("main_employer")

    return render(request, "register_employer.html")


def admin_redirect(request):
    if request.user.is_superuser:
        return redirect(reverse('admin:index'))


def main_employer(request):
    return render(request, "index_company.html")


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
    главная страница для кандидатов
    """
    return render(request, "index_applicant.html")


def resumes_applicant(request):
    """
    Страница для applicant, где создается и выводиться резюме.
    """
    return render(request, "applicant_resumes.html", {"resumes": resume.get_all_resumes(request.user)})


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
    user = auth.check_user_role(request)
    if user == "applicant":
        template = "base_applicant.html"
    elif user == "company":
        template = "employer.html"

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
    Позже сделать так, чтобы в заместо 404 ошибка, переводило на главную страницу.
    """
    if vacancy.get_vacancy(request.user, vacancy_id) is None:
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
                "vacancy": vacancy.get_vacancy(request.user, vacancy_id),
                "error_message": "Не правильно введены данные, или что-то пошло не так!"
            })
        else:
            return redirect("vacancy_company")

    return render(request, "create_vacancy.html", {"vacancy": vacancy.get_vacancy(request.user, vacancy_id)})


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
    user = auth.check_user_role(request)
    if user == "applicant":
        template = "base_applicant.html"
    elif user == "company":
        template = "employer.html"

    if request.method == "POST":
        if not home_page.delete_me(request.user, request.POST.get("password")):
            return render(request, "delete_me.html", {"error_message": "Не правильный пароль",
                                                      "template": template})
        else:
            return redirect("index")

    return render(request, "delete_me.html", {"template": template})
