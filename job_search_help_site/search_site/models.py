from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone

phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',  # Уникальное имя обратной связи для групп
        related_query_name='customuser'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',  # Уникальное имя обратной связи для разрешений
        related_query_name='customuser'
    )

    class Meta:
        verbose_name_plural = "Пользователи"


class Applicant(models.Model):
    """
    Кандидат который будет подавать резюме компании
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(null=True, max_length=30)
    second_name = models.CharField(null=True, max_length=30)
    is_confirmed = models.BooleanField(default=False)
    phone = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True, null=True)
    image = models.ImageField(upload_to="", null=True)

    class Meta:
        verbose_name_plural = "Кандитаты"


class Resume(models.Model):
    """
    Резюме, которое будет подаваться компании кандидатом
    """
    # ТУТ СДЕЛАТЬ ТОЖЕ ЧТОБЫ МОЖНО БЫЛО ПОДНИМАТЬ РЕЗЮМЕ КАК В МОДЕЛИ Vacancy!!!!
    name_of_resume = models.CharField(max_length=50, verbose_name="Название резюме", null=False)
    gender = models.CharField(max_length=10, verbose_name="Пол", null=False)
    # location = models.CharField(max_length=100, verbose_name="Местоположение, null=True)
    education = models.CharField(max_length=30, null=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления резюме")
    about_applicant = models.CharField(blank=True, null=True, max_length=500)
    profession = models.TextField(verbose_name="Профессия", null=False)
    key_skills = models.TextField(verbose_name="Ключевые навыки", null=False)
    place_of_work = models.CharField(max_length=30, null=True, verbose_name="Место работы")
    experience = models.CharField(max_length=15, verbose_name="Опыт работы", null=True)
    salary = models.CharField(max_length=30, null=True, verbose_name="Заработная плата")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="Кандидат")

    class Meta:
        verbose_name_plural = "Резюме"
        ordering = ["-updated_at"]  # возможно нужно будет по другому !!!!


class Company(models.Model):
    """
    Компания, которая будет публиковать вакансии
    """
    title_company = models.CharField(max_length=20, null=False, verbose_name="Название компании")
    name_user = models.CharField(max_length=30, null=False)
    second_name_user = models.CharField(max_length=30, null=False)
    phone_company = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True, null=True)
    description_company = models.CharField(max_length=500, null=True, verbose_name="Описание компании")
    image_company = models.ImageField(upload_to="", null=True)
    is_confirmed = models.BooleanField(default=False, verbose_name="Потверждена")

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Компании"


class Vacancy(models.Model):
    """
    Вакансии, которые будут подаваться компаниями
    """
    title_vacancy = models.CharField(max_length=50, null=False, verbose_name="Название вакансии")
    location = models.CharField(max_length=100, verbose_name="Место положение", null=True)
    salary = models.CharField(max_length=30, null=True, verbose_name="Заработная плата")
    experience = models.CharField(max_length=30, null=True, verbose_name="Опыт работы")
    description = models.CharField(max_length=500, verbose_name="Описание вакансии", null=False)
    type_of_employment = models.CharField(max_length=30, verbose_name="Тип занятости", null=True)
    specialization = models.CharField(max_length=30, verbose_name="Специализация", null=True)
    key_skills = models.CharField(max_length=100, verbose_name="Ключевые навыки", null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="Время обновления вакансии")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    # is_confirmed = models.BooleanField(default=True, verbose_name="Проверено")  #мб еще поле сделать чтобы админ мог проверять и потверждать

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Вакансии"
        ordering = ["-is_published", "-updated_at", "-created_at"]


class Application(models.Model):
    """
    Отклики на вакансию.
    """
    company = models.CharField(max_length=30, default="", verbose_name="Название компании")
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="Кандидат")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, verbose_name="Вакансия")
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, verbose_name="Резюме кандидата")
    application_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отклика")
    cover_letter = models.TextField(verbose_name="Сопроводительное письмо", null=True)
    is_invited = models.BooleanField(default=False, verbose_name="Приглашение отправлено")
    hidden = models.BooleanField(default=False, verbose_name="Отклик спрятан")
    status = models.CharField(
        max_length=10,
        choices=(
            ('reject', 'Reject'),
            ('access', 'Access'),
            ('pending', 'Pending'),
        ),
        null=False,
        default="pending",
        verbose_name="Статус отклика"
    )

    class Meta:
        verbose_name_plural = "Отправка резюме"


class LikeVacancyUser(models.Model):
    """
    Модель вакансий понравившихся пользователям.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Понравившиеся вакансии пользователей"
        unique_together = ('user', 'vacancy')


class LikeResumeUser(models.Model):
    """
    Модель резюме, понравившимся пользователям.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Понравившиеся резюме пользователей"
        unique_together = ('user', 'resume')


class RequestToVerificationUser(models.Model):
    """
    Model to verification user role.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(null=False, max_length=15, verbose_name="Role of user")
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Date of create request")

    class Meta:
        ordering = ["-date_created"]
        verbose_name_plural = "Запрос на верификацию пользователя"
