from django.contrib.auth import logout
from django.shortcuts import render, redirect

from search_site.services import auth


def index(request):
    return render(request, "index.html")


def help_for_people(request):
    return render(request, "help.html")


def login_applicant(request):
    """
    авторизация кандидата по url login/applicant
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
    return render(request, "index_applicant.html")
