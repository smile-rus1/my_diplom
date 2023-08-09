from django.core.exceptions import ObjectDoesNotExist

from search_site import models


def change_info_about_applicant(user, user_data: dict) -> bool:
    try:
        applicant = get_applicant(user)

        applicant.user.email = user_data["email"]
        applicant.first_name = user_data["first_name"]
        applicant.second_name = user_data["second_name"]
        applicant.phone = user_data["phone"]
        applicant.image = user_data["photo"]

        applicant.save()
        applicant.user.save()
        return True

    except ObjectDoesNotExist as e:
        print("ObjectDoesNotExist:", e)
        return False

    except Exception as e:
        print("Error:", e)
        return False


def get_applicant(user) -> models.Applicant:
    applicant = models.Applicant.objects.get(user=user)

    return applicant

