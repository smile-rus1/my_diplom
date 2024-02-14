from django.contrib import admin
from . import models


@admin.register(models.VerificationUserRole)
class ApplicantAdmin(admin.ModelAdmin):
    pass

