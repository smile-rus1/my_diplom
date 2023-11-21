from django.http import Http404
from django.urls import reverse_lazy

from search_site import models
from . import send_mail_to_users


def get_all_responded_to_vacancy(user: models.CustomUser) -> models.Application:
    """
    Возвращает всех кандидатов, которые откликнулись на вакансии.
    """
    return models.Application.objects \
        .filter(applicant__isnull=False).select_related("applicant__user", "vacancy__company") \
        .filter(vacancy__company=user.company).order_by("-application_date")


def show_all_info_about_applicant_of_application(
        user: models.CustomUser,
        applicant_id: int,
        vacancy_id: int
) -> models.Application:
    """
    Показывает всю инфомацию о applicant, которые откликнулись на вакансию.
    """
    try:
        return models.Application.objects \
            .filter(applicant__isnull=False)\
            .select_related("applicant__user", "vacancy__company") \
            .filter(vacancy__company=user.company, applicant=applicant_id, vacancy=vacancy_id).first()

    except:
        raise Http404("Не найдено")


def show_all_info_about_applicant(resume_id: int) -> models.Resume:
    """
    Показывает всю информацию о кандидате по переданному
    """
    return models.Resume.objects.filter(id=resume_id).select_related("applicant__user").first()


def change_application_status_of_applicant(**user_data) -> None:
    """
    Меняет status у applicant по id вакансии.
    """
    application = models.Application.objects.filter(id=user_data.get("application_id"))
    application.update(status=user_data.get("status"))

    if not application:
        return

    link_to_redirect = user_data.get("request").build_absolute_uri(
        reverse_lazy("vacancy", kwargs={"vacancy_id": application.first().vacancy.id})
    )

    if user_data.get("status") == "access":
        send_mail_to_users.send_mail_to_users(
            subject=f"Компания пригласила вас на интервью",
            message=f"«Здравствуйте\n"
                    f"Благодарим Вас, за отклик на вакансию {application.first().vacancy.title_vacancy}, "
                    f"наши специалисты рассмотрят Ваше резюме и сообщат о решении.\n"
                    f"С уважением {application.first().vacancy.company.name_user}»\n"
                    f"\nВакансия: {application.first().vacancy.title_vacancy}\n"
                    f"\n\nСсылка для перехода: {link_to_redirect}",
            email_recipient=f"{application.first().applicant.user.email}"
        )

    elif user_data.get("status") == "reject":
        send_mail_to_users.send_mail_to_users(
            subject=f"Компания не готова пригласить вас на интервью",
            message=f"«Здравствуйте\n"
                    f"Мы ознокомились с Вашим резюме и к сожалению "
                    f"не готовы пригласить Вас на дальнейшее собеседование по этой вакансии. "
                    f"Возможно в будующем, мы вернемся к вашей кандидатуре, если у нас возникнет потребность.\n"
                    f"С уважением {application.first().vacancy.company.name_user}»\n"
                    f"\nВакансия: {application.first().vacancy.title_vacancy}\n"
                    f"\n\nСсылка для перехода: {link_to_redirect}",
            email_recipient=f"{application.first().applicant.user.email}"
        )


def create_invitation_to_applicant(request, resume_id: int, vacancy: str) -> None:
    """
    Присылает приглашение кандидату от компании.
    """
    resume = models.Resume.objects.filter(id=resume_id).select_related("applicant").first()
    vacancy = models.Vacancy.objects.filter(title_vacancy=vacancy, company=request.user.company).first()

    models.Application.objects.create(
        applicant=resume.applicant,
        vacancy=vacancy,
        resume=resume,
        cover_letter="",
        company=vacancy.company.title_company,
        status="access"
    )
    link_to_redirect = request.build_absolute_uri(
        reverse_lazy("vacancy", kwargs={"vacancy_id": vacancy.id})
    )

    send_mail_to_users.send_mail_to_users(
        subject=f"Компания пригласила вас на интервью",
        message=f"Компания {vacancy.company.title_company} пригласила вас на интервью."
                f"\nВакансия: {vacancy.title_vacancy}\n"
                f"Ссылка для перехода: {link_to_redirect}",
        email_recipient=f"{resume.applicant.user.email}"
    )


def get_is_applied_respond_from_company(user: models.CustomUser) -> list[models.Vacancy]:
    """
    Проверяет сделала ли отклик уже компания кандидату.
    """
    lst_apply_respond = [
        ls.vacancy for ls in models.Application.objects.filter(
            is_invited=True,
            vacancy__company__user=user,
        )
    ]
    return lst_apply_respond
