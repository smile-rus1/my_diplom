from django.contrib.auth import login

from search_site.models import CustomUser


def register_applicant(email: str, password1: str):
    user = CustomUser(email=email)
    user.set_password(password1)
    user.save()
    return True


def match_password(password1: str, password2: str):
    if password1 != password2:
        return False
    return True


def is_valid_password(password1: str):
    if len(password1) < 8:
        return False

    if not any(char.isdigit() for char in password1):
        return False

    return True


def is_not_exists_email(email: str):
    if CustomUser.objects.filter(email=email).exists():
        return False
    return True
