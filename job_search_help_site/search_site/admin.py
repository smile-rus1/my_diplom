from django.contrib import admin

from search_site import models


"""
ПОТОМ ЗАНЯТЬСЯ АДМИНКОЙ!!!!
"""


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", )


@admin.register(models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    search_fields = ("email", )


@admin.register(models.Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    # Добавьте поля, которые хотите отображать для модели Applicant
    pass


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    # Добавьте поля, которые хотите отображать для модели Company
    pass


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    # Добавьте поля, которые хотите отображать для модели Resume
    pass


@admin.register(models.Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    # Добавьте поля, которые хотите отображать для модели Vacancy
    pass