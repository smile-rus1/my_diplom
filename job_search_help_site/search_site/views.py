from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from search_site.services import register


def index(request):
    return render(request, "index.html")


def help_for_people(request):
    return render(request, "help.html")


def login_applicant(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Неправильный email или пароль."
            return render(request, 'login_applicant.html', {'error_message': error_message})

    return render(request, "login_applicant.html")


def register_applicant(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if not register.match_password(password1, password2):
            messages.error(request, 'Пароли не совпадают')
            return redirect('register_applicant')

        if not register.is_valid_password(password1):
            messages.error(request, "Пароль должен состоять из 8 символов и в нем должны быть буквы!")
            return redirect('register_applicant')

        if not register.is_not_exists_email(email):
            messages.error(request, "Такой email уже зарегистрирован!")
            return redirect("register_applicant")

        register.register_applicant(email, password1)
        user = authenticate(request, email=email, password=password1)
        if user is not None:
            login(request, user)

        return redirect("login_applicant")

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
