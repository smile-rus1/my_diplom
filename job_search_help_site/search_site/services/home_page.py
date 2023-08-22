from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from search_site import models


def change_info_about_applicant(user: models.CustomUser, user_data: dict) -> bool:
    try:
        applicant = get_applicant(user)

        applicant.user.email = user_data.get("email")
        applicant.first_name = user_data.get("first_name")
        applicant.second_name = user_data.get("second_name")
        applicant.phone = user_data.get("phone")
        applicant.image = user_data.get("photo") if user_data.get("photo") \
                                                                  is not None else applicant.image

        applicant.save()
        applicant.user.save()
        return True

    except ObjectDoesNotExist as e:
        print("ObjectDoesNotExist:", e)
        return False

    except Exception as e:
        print("Error:", e)
        return False


def change_info_about_company(user: models.CustomUser, user_data: dict) -> bool:
    """
    Изменяет иформацию компании.
    """
    try:
        company = get_company(user)

        company.user.email = user_data.get("email")
        company.name_user = user_data.get("name_user")
        company.second_name_user = user_data.get("second_name_user")
        company.title_company = user_data.get("title_company")
        company.phone_company = user_data.get("phone_company")
        company.description_company = user_data.get("description_company")
        company.image_company = user_data.get("image_company") if user_data.get("image_company") \
                                                                  is not None else company.image_company

        company.save()
        company.user.save()
        return True

    except ObjectDoesNotExist as e:
        print("ObjectDoesNotExist:", e)
        return False

    except Exception as e:
        print("Error:", e)
        return False


def get_applicant(user) -> models.Applicant | None:
    try:
        applicant = models.Applicant.objects.get(user=user)
        return applicant

    except:
        return get_company(user)


def get_company(user):
    return models.Company.objects.get(user=user)


def user_change_password(request, user: models.CustomUser, user_data: dict):
    if user.check_password(user_data["current_password"]):
        user.set_password(user_data["new_password"])
        user.save()

        login(request, user)
    else:
        return

    return True
