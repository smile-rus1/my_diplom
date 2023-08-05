from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
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


class Specialization(models.Model):
    name_specialization = models.TextField()

    class Meta:
        verbose_name_plural = "Специализация"


class Education(models.Model):
    name_of_education = models.CharField(max_length=30, null=False)

    class Meta:
        verbose_name_plural = "Образование"


class TypeEmployment(models.Model):
    name_type_of_employment = models.CharField(max_length=30, null=False)

    class Meta:
        verbose_name_plural = "Тип занятости"


class Applicant(models.Model):
    """
    Кандидат который будет подавать резюме компании
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Кандитаты"


class Resume(models.Model):
    """
    Резюме, которое будет подаваться компании кандидатом
    """
    # ТУТ СДЕЛАТЬ ТОЖЕ ЧТОБЫ МОЖНО БЫЛО ПОДНИМАТЬ РЕЗЮМЕ КАК В МОДЕЛИ Vacancy!!!!
    name = models.CharField(max_length=30, null=False)
    second_name = models.CharField(max_length=30, null=False)
    last_name = models.CharField(max_length=30, null=False)
    gender = models.CharField(max_length=10, verbose_name="Пол")
    education = models.ForeignKey(Education, on_delete=models.SET_NULL, null=True, verbose_name="Образование")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Время обновления")

    phone = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True)
    image = models.ImageField(upload_to="", null=True)
    profession = models.TextField()

    key_skills = models.ForeignKey(Specialization, on_delete=models.CASCADE, verbose_name="Ключевые навыки")

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE, verbose_name="Кандидат")

    class Meta:
        verbose_name_plural = "Резюме"
        ordering = ["-updated_at"]  # возможно нужно будет по другому !!!!


class Company(models.Model):
    """
    Компания, которая будет публиковать вакансии
    """
    name_company = models.CharField(max_length=20, null=False, unique=True)
    name_user = models.CharField(max_length=30, null=False)
    second_name_user = models.CharField(max_length=30, null=False)
    phone_company = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True, null=True)
    image_company = models.ImageField(upload_to="", null=True)
    is_confirmed = models.BooleanField(default=False)

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Компании"


class Vacancy(models.Model):
    """
    Вакансии, которые будут подаваться компаниями
    """
    name_vacancy = models.CharField(max_length=50, null=False)
    town = models.CharField(max_length=30, null=False)
    salary = models.CharField(max_length=30)
    experience = models.CharField(max_length=30)
    description = models.CharField(max_length=300, verbose_name="Описание вакансии")
    created_at = models.DateTimeField(auto_now_add=True)
    publication_time = models.DateTimeField(default=timezone.now)  # либо использовать default=timezone.now
    location = models.CharField(max_length=100)

    type_of_employment = models.ForeignKey(TypeEmployment, on_delete=models.SET_NULL, null=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Вакасии"
        ordering = ["-publication_time"]


class Application(models.Model):
    company = models.CharField(max_length=100, default="")
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Отправка резюме"
