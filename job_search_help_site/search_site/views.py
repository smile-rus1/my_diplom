from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.urls import reverse

from .services import auth, home_page, resume


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
    return render(request, "applicant_resumes.html", {"resumes": resume.get_resume(request.user)})


def applicant_home_page(request):
    """
    домашняя страница applicant.
    P.S. Доработать request.FILES['image'] (чтобы файлы принимались по другому т.к. если
    частично обновлять, то keyerror будет!!!!)
    """
    if request.method == "POST":
        if home_page.change_info_about_applicant(
                request.user,
                {
                    "email": request.POST.get('email'),
                    "first_name": request.POST.get("first_name"),
                    "second_name": request.POST.get("second_name"),
                    "phone": request.POST.get("phone"),
                    "photo": request.FILES.get('image')
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
    страница на которой пользователь
    изменяет свой пароль.
    """
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
                return render(request, "change_password.html", {'error_message': "Не правильно введен пароль!"})
            else:
                return render(request, "change_password.html", {'successful_message': "Пароль изменен!"})

        else:
            return render(request, 'change_password.html', {'error_message': "Пароли не совпадают!"})

    return render(request, "change_password.html")


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
    if request.method == "POST":
        if resume.update_resume(
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
            return redirect("rezume_applicant")

    return render(request, "create_resume.html", {"resume": resume.get_applicant_resume(resume_id)})


def vacancy_company(request):

    return render(request, "company_vacancy.html")
