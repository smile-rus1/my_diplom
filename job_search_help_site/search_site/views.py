from django.contrib.auth import logout
from django.shortcuts import render, redirect

from search_site.services import auth
from search_site.services import home_page


def index(request):
    """
    начальная страница на сайте.
    """
    return render(request, "index.html")


def help_for_people(request):
    if request.user.is_authenticated:
        user = auth.check_user(request)
        if user == "applicant":
            return render(request, "help.html", {"type": "applicant"})
        elif user == "company":
            return

    return render(request, "help.html")


def login_applicant(request):
    """
    авторизация кандидата по url login/applicant.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not auth.login_user(request, {"email": email, "password": password}):
            error_message = "Неправильный email или пароль!"
            return render(request, 'login_applicant.html', {'error_message': error_message})
        else:
            return redirect("main_applicant")

    return render(request, "login_applicant.html")


def register_applicant(request):
    """
    регистрация кандидата по url register/applicant
    еще будет меняться т.к. не настроил модельки еще!
    """
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not auth.register_user(request, email, password1, password2, "applicant"):
            return redirect("register_applicant")
        else:
            return redirect("main_applicant")

    return render(request, "register_applicant.html")


def index_employer(request):
    return render(request, "index_employer.html")


def login_employer(request):
    return render(request, "login_employer.html")


def register_employer(request):
    return render(request, "register_employer.html")


def logout_user(request):
    logout(request)
    return redirect("index")


def main_applicant(request):
    """
    главная страница для кандидатов
    """
    return render(request, "index_applicant.html")


def resumes_applicant(request):
    return render(request, "applicant_resumes.html")


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
    создание резюме кандидата
    """
    if request.method == "POST":
        ...
        # print(request.POST.get("profession"))
        # print(request.POST.get("skills").split())
    return render(request, "create_resume.html")
