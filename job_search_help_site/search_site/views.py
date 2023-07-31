from django.shortcuts import render, redirect


def index(request):
    return render(request, "index.html")


def help_for_people(request):
    return render(request, "help.html")


def login_applicant(request):
    return render(request, "login_applicant.html")


def register_applicant(request):
    if request.method == "POST":
        print("POST METHOD")
        return redirect("login_applicant")

    return render(request, "register_applicant.html")


def index_employer(request):
    return render(request, "index_employer.html")


def login_employer(request):
    return render(request, "login_employer.html")
