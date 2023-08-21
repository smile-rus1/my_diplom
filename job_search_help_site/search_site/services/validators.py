from django.core.exceptions import ValidationError


def validate_salary(salary, currency):
    """
    Валидирует з/п applicanta.
    """
    if salary == "":
        return None

    return salary + " " + currency


def validate_experience(experience: int) -> str | None:
    """
    Валидирует experience по годам и приставляет суффикс взависимости от кол-ва.
    """
    if not experience:
        return

    experience = int(experience)
    if 1 <= experience <= 4:
        if experience == 1:
            expected_suffix = "год"
        else:
            expected_suffix = "года"
    elif 5 <= experience <= 20:
        expected_suffix = "лет"
    elif 21 <= experience <= 24:
        expected_suffix = "год"
    else:
        raise ValidationError("Некорректный опыт работы")

    return f"{experience} {expected_suffix}"
