from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def rb(request):
    return render(request, "rb.html")


def help_for_people(request):
    return render(request, "help.html")
