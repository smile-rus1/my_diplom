from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def help_for_people(request):
    return render(request, "help.html")


def login_applicant(request):
    return render(request, "login_applicant.html")


def register_applicant(request):
    return render(request, "register_applicant.html")
