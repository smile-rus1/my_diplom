from search_site import models


def change_application_on_user_of_list_active(application_id: int) -> None:
    """
    Удаляет отклик у пользователя.
    """
    application = models.Application.objects.filter(id=application_id).first()
    application.hidden = not application.hidden
    application.save()


def reject_invitation_from_company():
    """
    Отклоняет приглашение от компании.
    """
    # Тут реализовать логику, которая будет отклонять приглашение от компании, путем изменения либо состояния,
    # либо путем удаления или же просто путем как компания может сделать reject, так и кандидату дать такую возможность
    return NotImplementedError
