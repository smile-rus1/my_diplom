from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def help_for_people(request):
    return render(request, "help.html")
